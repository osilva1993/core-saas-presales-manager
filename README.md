# 🎯 CoreSaaS Pre-Sales Manager — Agentic AI Copilot

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit UI](https://img.shields.io/badge/frontend-Streamlit-red.svg)](https://streamlit.io/)
[![Groq LPU](https://img.shields.io/badge/llm_engine-Groq_API-flash.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Agente autônomo B2B de Inteligência Comercial e Pré-Vendas**, projetado para automatizar pesquisas de leads, levantamento de sinais de mercado e geração de dossiês estratégicos de prospeção em segundos.

---

## 💡 O Problema & A Solução

* **A Dor do Negócio:** SDRs e BDRs sêniores gastam entre **15 a 30 minutos por prospect** navegando em sites, LinkedIn e notícias para entender o momento da empresa, mapear dores do cargo e criar copys personalizadas.
* **A Solução Agêntica:** O **CoreSaaS Pre-Sales Manager** executa chamadas de ferramentas de busca (*Function Calling*), analisa o contexto comercial do prospect e entrega um **Dossiê Comercial Completo** acompanhado de cadência multicanal (E-mail, LinkedIn e Cold Call) em **menos de 5 segundos**.

---

## 🏗️ Arquitetura do Sistema & Fluxo de Dados

O projeto utiliza um padrão agêntico com **Function Calling de dois passos (Two-Pass Synthesis)**, garantindo a execução de ferramentas em tempo de execução e a normalização do histórico de chat.

```mermaid
graph TD
    A[👤 SDR / Usuário] -->|Insere Prompt/Dados| B[💻 Streamlit Chat Interface]
    B -->|Envio de Histórico + Tool Schemas| C[⚡ Groq LPU Engine / openai/gpt-oss-120b]
    
    C -->|Solicita Tool: pesquisar_sinais_e_empresa| D[🛡️ Parameter Sanitizer & Inspector]
    D -->|Executa Invocação Segura| E[🔍 Signal Tracker Connector]
    E -->|Retorna Payload JSON com Sinais| D
    
    D -->|Injeta Tool Response no Histórico| C
    C -->|Síntese Final baseada nas System Instructions| B
    B -->|Exibe Dossiê + Cadência no Chat| A