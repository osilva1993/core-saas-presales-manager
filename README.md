# 🎯 CoreSaaS Pre-Sales Manager — Agentic AI Copilot

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit UI](https://img.shields.io/badge/frontend-Streamlit-red.svg)](https://streamlit.io/)
[![Groq LPU](https://img.shields.io/badge/llm_engine-Groq_API-flash.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Agente Autônomo B2B de Inteligência Comercial e Pré-Vendas**, projetado para automatizar a pesquisa de prospects, consolidação de sinais de mercado e geração de dossiês estratégicos com cadência multicanal em menos de 5 segundos.

---

## 💡 O Problema & O Impacto no Dia a Dia de Vendas

* **O Gargalo Operacional:** SDRs e BDRs sêniores gastam entre **15 e 30 minutos por prospect** navegando em sites, LinkedIn e notícias para entender o momento da empresa, mapear dores do cargo e redigir abordagens personalizadas.
* **A Solução Agêntica:** O **CoreSaaS Pre-Sales Manager** atua como um copilot de vendas de alta performance. Ele orquestra buscas em tempo real, consulta uma base especialista de habilidades comerciais e entrega um **Dossiê Comercial Completo** acompanhado de cadências acionáveis (E-mail, LinkedIn e Cold Call).

---

## 🧠 Biblioteca de Skills & Potencializador de Prospecção

O grande diferencial funcional do agente está na sua **arquitetura de skills desacopladas** em Markdown (`skills/`). Cada habilidade representa um especialista virtual que orienta o agente na execução de etapas críticas da prospecção:

| Skill Especialista | Função Prática na Prospecção | Impacto na Rotina Comercial |
| :--- | :--- | :--- |
| 🔍 **Signal Tracker** | Mapeia gatilhos temporais (contratações, novas rodadas de investimento, expansão de equipe). | Permite abordagens baseadas em **timing perfeito** e eventos reais. |
| 📊 **Commercial Research** | Consolida o modelo de negócio da empresa, público-alvo, presença no mercado e concorrência. | Elimina a necessidade de navegação manual em múltiplos sites. |
| 🎯 **Framework Selector** | Seleciona automaticamente a metodologia ideal (SPIN Selling, BANT, Challenger, MEDDIC) baseada no perfil da conta. | Garante rigor metodológico sem exigir que o SDR monte o script do zero. |
| 🧩 **Product Advisor** | Faz o *cross-matching* entre as dores diagnosticadas e o portfólio de soluções SaaS. | Apresenta o produto diretamente como solução para o problema identificado. |
| ✍️ **Outbound Copy** | Gera e-mails de alta conversão e mensagens de LinkedIn focadas na dor específica da persona. | Fim dos templates genéricos; copys personalizadas em segundos. |
| 📞 **Cold Call Strategy** | Cria roteiros de ligação estruturados com ganchos de abertura e contorno de objeções frequentes. | Prepara o pré-vendedor para ligações com maior taxa de agendamento. |
| 🗓️ **Campaign Builder** | Estrutura a cadência temporal multicanal (Touchpoints ao longo dos dias). | Organiza a execução diária do SDR em um fluxo lógico e replicável. |

---

## 🏗️ Arquitetura do Sistema & Fluxo de Dados

O projeto utiliza o padrão agêntico com **Function Calling de dois passos (Two-Pass Synthesis)**, garantindo a execução de ferramentas em tempo de execução e a normalização do histórico de chat.

```mermaid
graph TD
    A[👤 SDR / Usuário] -->|Insere Prompt/Dados| B[💻 Streamlit Chat Interface]
    B -->|Envio de Histórico + Tool Schemas| C[⚡ Groq LPU Engine / gpt-oss-120b]
    
    C -->|Solicita Tool: pesquisar_sinais_e_empresa| D[🛡️ Parameter Sanitizer & Inspector]
    D -->|Executa Invocação Segura| E[🔍 Signal Tracker Connector]
    E -->|Retorna Payload JSON com Sinais| D
    
    D -->|Injeta Tool Response no Histórico| C
    C -->|Síntese Final baseada nas System Instructions + Skills| B
    B -->|Exibe Dossiê + Cadência no Chat| A