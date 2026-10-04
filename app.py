import streamlit as st
import json
import os
import inspect
from dotenv import load_dotenv
from groq import Groq

from mock_connectors.websearch_mock import pesquisar_sinais_e_empresa

# Configuração da página
st.set_page_config(
    page_title="CoreSaaS Pre-Sales Chat",
    page_icon="💬",
    layout="wide"
)

st.title("💬 CoreSaaS — Copilot de Pré-Vendas B2B")
st.caption("Converse com o agente de inteligência comercial para pesquisar leads, analisar dores e refinar copys.")

load_dotenv(override=True)
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("❌ `GROQ_API_KEY` não encontrada no `.env`.")
    st.stop()

client = Groq(api_key=groq_api_key)

# 1. Carrega as Instruções do Sistema
caminho_instrucoes = os.path.join("instructions", "system_instructions.md")
if os.path.exists(caminho_instrucoes):
    with open(caminho_instrucoes, "r", encoding="utf-8") as f:
        system_instruction = f.read()
else:
    system_instruction = "Você é um especialista em pré-vendas B2B."

# 2. Inicializa o Histórico da Conversa
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_instruction}
    ]

# 3. Barra Lateral: Atalhos e Limpeza
with st.sidebar:
    st.header("⚡ Atalho de Prospecção")
    empresa = st.text_input("Empresa", value="Coca-Cola")
    nome_lead = st.text_input("Lead", value="Bruno")
    cargo = st.text_input("Cargo", value="Gerente de Atendimento")
    
    if st.button("🚀 Iniciar Prospecção", type="primary"):
        prompt_inicial = f"Vou prospectar o {nome_lead} que trabalha na {empresa}, ele é {cargo}."
        st.session_state.messages.append({"role": "user", "content": prompt_inicial})
        st.rerun()

    st.divider()
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = [{"role": "system", "content": system_instruction}]
        st.rerun()

# 4. Exibe apenas as mensagens do Usuário e do Assistente no Chat
for msg in st.session_state.messages:
    if isinstance(msg, dict):
        role = msg.get("role")
        content = msg.get("content")
    else:
        role = getattr(msg, "role", None)
        content = getattr(msg, "content", None)

    # Exibe apenas mensagens de conversa na UI (ignora 'system' e chamadas 'tool')
    if role in ["user", "assistant"] and content:
        with st.chat_message(role):
            st.markdown(content)

# 5. Entrada do Usuário
if user_input := st.chat_input("Digite sua solicitação (ex: 'Encurte o e-mail' ou 'Crie objeções de venda')..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()

# 6. Execução do Agente se a última mensagem for do Usuário
if st.session_state.messages[-1].get("role") == "user":
    with st.chat_message("assistant"):
        with st.status("🧠 Agente analisando...", expanded=True) as status:
            
            MODELO_ALVO = "openai/gpt-oss-120b"
            available_functions = {"pesquisar_sinais_e_empresa": pesquisar_sinais_e_empresa}

            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "pesquisar_sinais_e_empresa",
                        "description": "Busca sinais de mercado, notícias recentes e dados sobre a empresa e o lead.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "empresa": {"type": "string"},
                                "cargo": {"type": ["string", "null"]},
                                "nome_lead": {"type": ["string", "null"]}
                            },
                            "required": ["empresa"]
                        }
                    }
                }
            ]

            try:
                response = client.chat.completions.create(
                    model=MODELO_ALVO,
                    messages=st.session_state.messages,
                    tools=tools,
                    tool_choice="auto",
                    temperature=0.2
                )

                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls

                # Se o agente decidiu executar a ferramenta
                if tool_calls:
                    # Converte o objeto de chamada em dicionário seguro
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response_message.content,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            } for tc in tool_calls
                        ]
                    })

                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_to_call = available_functions[function_name]
                        function_args = json.loads(tool_call.function.arguments)

                        cleaned_args = {k: v for k, v in function_args.items() if v is not None}
                        sig = inspect.signature(function_to_call)
                        has_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
                        filtered_args = cleaned_args if has_kwargs else {k: v for k, v in cleaned_args.items() if k in sig.parameters}

                        status.write(f"🔍 Consultando ferramenta `{function_name}`...")
                        function_response = function_to_call(**filtered_args)

                        st.session_state.messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps(function_response, ensure_ascii=False)
                        })

                    status.write("✍️ Processando inteligência e gerando resposta...")
                    second_response = client.chat.completions.create(
                        model=MODELO_ALVO,
                        messages=st.session_state.messages,
                        temperature=0.3
                    )
                    bot_reply = second_response.choices[0].message.content
                else:
                    bot_reply = response_message.content

                status.update(label="✅ Concluído!", state="complete", expanded=False)
                
                # Exibe e grava no histórico do chat
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})

            except Exception as e:
                status.update(label="❌ Erro!", state="complete", expanded=False)
                st.error(f"Erro na execução: {e}")