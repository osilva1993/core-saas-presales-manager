import inspect
from mock_connectors.websearch_mock import pesquisar_sinais_e_empresa

def test_pesquisar_sinais_e_empresa_retorno_valido():
    """Valida se a busca do Signal Tracker retorna a estrutura de dados esperada."""
    resultado = pesquisar_sinais_e_empresa(empresa="Coca-Cola", cargo="Gerente de Atendimento", nome_lead="Bruno")
    
    assert isinstance(resultado, dict)
    assert resultado["empresa"] == "Coca-Cola"
    assert resultado["lead"] == "Bruno"
    assert resultado["cargo"] == "Gerente de Atendimento"
    assert "sinais_mercado" in resultado
    assert len(resultado["sinais_mercado"]) > 0

def test_inspecao_kwargs_funcao_mock():
    """Garante que a função aceita **kwargs dinâmicos para prevenir erros de schema do LLM."""
    sig = inspect.signature(pesquisar_sinais_e_empresa)
    has_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
    
    assert has_kwargs is True