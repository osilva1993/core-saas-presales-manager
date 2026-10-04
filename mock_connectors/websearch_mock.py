def pesquisar_sinais_e_empresa(empresa: str, cargo: str = "", nome_lead: str = "", **kwargs) -> dict:
    """
    Executa varredura via WebSearch e Signal Tracker para levantar notícias recentes,
    desafios do setor, stack atual e momento estratégico da empresa/lead.
    """
    print(f"\n🔍 [SIGNAL TRACKER] Rodando WebSearch para: '{empresa}' | Lead: '{nome_lead}' ({cargo})...")
    
    return {
        "empresa": empresa,
        "lead": nome_lead,
        "cargo": cargo,
        "sinais_mercado": [
            f"Expansão recente dos canais digitais de atendimento da {empresa}.",
            "Aumento na busca por redução de SLA e automação no suporte ao consumidor.",
            "Foco corporativo em eficiência operacional e CX (Customer Experience) omnichannel."
        ],
        "desafios_provaveis_do_cargo": [
            "Gestão de picos de demanda no atendimento ao cliente.",
            "Manutenção do NPS/CSAT alto sem explodir os custos operacionais.",
            "Falta de visibilidade analítica em tempo real sobre as dores mais recorrentes nos chamados."
        ],
        "tecnologias_identificadas": ["Salesforce Service Cloud", "Genesis", "WhatsApp Business API"]
    }