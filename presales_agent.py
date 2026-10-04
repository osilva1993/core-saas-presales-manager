import os
import sys
import json
import inspect
from dotenv import load_dotenv
from groq import Groq

from mock_connectors.websearch_mock import pesquisar_sinais_e_empresa

load_dotenv(override=True)

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    print("❌ ERRO CRÍTICO: GROQ_API_KEY não encontrada no arquivo .env!")
    sys.exit(1)

client = Groq(api_key=groq_api_key)

def executar_pesquisa_presales(consulta_usuario: str):
    print(f"\n Requisição de Pesquisa: '{consulta_usuario}'")
    
    caminho_instrucoes = os.path.join("instructions", "system_instructions.md")
    if not os.path.exists(caminho_instrucoes):
        print(f"❌ ERRO: Arquivo de instruções não encontrado em '{caminho_instrucoes}'.")
        return

    with open(caminho_instrucoes, "r", encoding="utf-8") as f:
        system_instruction = f.read()

    MODELO_ALVO = "openai/gpt-oss-120b"

    available_functions = {
        "pesquisar_sinais_e_empresa": pesquisar_sinais_e_empresa
    }

    tools = [
        {
            "type": "function",
            "function": {
                "name": "pesquisar_sinais_e_empresa",
                "description": "Busca sinais de mercado, notícias recentes e dados sobre a empresa e o lead.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "empresa": {
                            "type": "string",
                            "description": "Nome da empresa alvo (ex: Coca-Cola)"
                        },
                        "cargo": {
                            "type": ["string", "null"],
                            "description": "Cargo do prospect (ex: Gerente de Atendimento)"
                        },
                        "nome_lead": {
                            "type": ["string", "null"],
                            "description": "Nome do prospect/lead"
                        }
                    },
                    "required": ["empresa"]
                }
            }
        }
    ]

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": consulta_usuario}
    ]

    try:
        # 1. Primeiro Passe: Invocação do modelo com Function Calling
        response = client.chat.completions.create(
            model=MODELO_ALVO,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.2
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                # Sanitização: remove chaves com valor None/null
                cleaned_args = {k: v for k, v in function_args.items() if v is not None}

                # Inspeção segura de parâmetros
                sig = inspect.signature(function_to_call)
                has_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
                filtered_args = cleaned_args if has_kwargs else {k: v for k, v in cleaned_args.items() if k in sig.parameters}

                # Executa a tool
                function_response = function_to_call(**filtered_args)

                # Anexa a resposta da tool no histórico da sessão
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response, ensure_ascii=False)
                })

            # 2. Segundo Passe: Síntese e geração do Dossiê Comercial Final
            second_response = client.chat.completions.create(
                model=MODELO_ALVO,
                messages=messages,
                temperature=0.3
            )

            print(f"\n DOSSIÊ COMERCIAL & COPYS DE ABORDAGEM:\n")
            print(second_response.choices[0].message.content)
        else:
            print(f"\n Resposta Direta:\n{response_message.content}")

    except Exception as e:
        print(f"\n ❌ ERRO AO EXECUTAR VIA GROQ: {e}")

if __name__ == "__main__":
    prompt_prospeccao = "Vou prospectar o Bruno que trabalha na Coca-Cola, ele é Gerente de Atendimento."
    executar_pesquisa_presales(prompt_prospeccao)