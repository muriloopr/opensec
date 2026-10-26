from datetime import datetime
from typing import Dict, Any

def calcular_custo_patio_veiculo(
    custo_aquisicao: float,
    preco_atual: float,
    data_entrada_str: str,
    taxa_capital_anual: float = 0.12,
    taxa_depreciacao_anual: float = 0.15,
    taxa_seguro_anual: float = 0.012
) -> Dict[str, Any]:
    """
    Calcula o custo diário e acumulado de carregar o veículo no pátio,
    avaliando regras de aging (>30 dias) e sugerindo reajuste dinâmico.
    """
    # Parse da data de entrada
    try:
        data_limpa = data_entrada_str.replace("Z", "").split(".")[0]
        if "T" in data_limpa:
            data_entrada = datetime.fromisoformat(data_limpa)
        elif " " in data_limpa:
            data_entrada = datetime.strptime(data_limpa, "%Y-%m-%d %H:%M:%S")
        else:
            data_entrada = datetime.strptime(data_limpa, "%Y-%m-%d")
    except Exception:
        data_entrada = datetime.now()

    dias_em_estoque = max(0, (datetime.now() - data_entrada).days)

    # Taxa diária composta (capital + depreciação + seguro)
    taxa_diaria = (taxa_capital_anual + taxa_depreciacao_anual + taxa_seguro_anual) / 365.0
    custo_diario = round(custo_aquisicao * taxa_diaria, 2)
    custo_patio_acumulado = round(custo_diario * dias_em_estoque, 2)

    # Gatilhos de aging e sugestão de desconto
    if dias_em_estoque <= 30:
        status_aging = "NORMAL"
        desconto_sugerido = 0.0
    elif dias_em_estoque <= 45:
        status_aging = "ALERTA_AMARELO"
        desconto_sugerido = round(min(preco_atual * 0.04, custo_patio_acumulado), 2)
    else:
        status_aging = "ALERTA_VERMELHO"
        desconto_sugerido = round(min(preco_atual * 0.07, custo_patio_acumulado * 1.25), 2)

    # Piso de segurança: margem mínima de 2% sobre o custo de aquisição
    piso_seguranca = round(custo_aquisicao * 1.02, 2)
    novo_preco_sugerido = round(preco_atual - desconto_sugerido, 2)

    if novo_preco_sugerido < piso_seguranca:
        novo_preco_sugerido = piso_seguranca
        desconto_sugerido = round(max(0.0, preco_atual - novo_preco_sugerido), 2)

    return {
        "dias_em_estoque": dias_em_estoque,
        "custo_diario": custo_diario,
        "custo_patio_acumulado": custo_patio_acumulado,
        "status_aging": status_aging,
        "desconto_sugerido": desconto_sugerido,
        "novo_preco_sugerido": novo_preco_sugerido,
        "piso_seguranca": piso_seguranca
    }
