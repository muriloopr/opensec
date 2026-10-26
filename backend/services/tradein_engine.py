from typing import Dict, Any

def calcular_tradein_margem_combinada(
    preco_venda_novo: float,
    custo_aquisicao_novo: float,
    preco_fipe_usado: float,
    custo_recondicionamento_est: float,
    valor_proposto_usado: float,
    margem_alvo_revenda: float = 0.15
) -> Dict[str, Any]:
    """
    Avalia a negociação de Trade-In calculando a oferta ideal, o overallowance concedido,
    a projeção de margem futura e a margem combinada consolidada da operação.
    """
    # 1. Perna do Carro em Estoque (Venda)
    lucro_bruto_novo = round(preco_venda_novo - custo_aquisicao_novo, 2)

    # 2. Perna do Carro Usado de Entrada (Trade-In)
    # Oferta ideal garante a margem de revenda futura descontando recondicionamento
    oferta_ideal_sugerida = round(preco_fipe_usado * (1.0 - margem_alvo_revenda) - custo_recondicionamento_est, 2)
    oferta_minima = round(preco_fipe_usado * (1.0 - margem_alvo_revenda - 0.05) - custo_recondicionamento_est, 2)
    oferta_maxima = round(preco_fipe_usado * (1.0 - 0.08) - custo_recondicionamento_est, 2)

    # Overallowance: valor pago além da oferta ideal recomendada
    overallowance = round(max(0.0, valor_proposto_usado - oferta_ideal_sugerida), 2)

    # Margem projetada na revenda futura do veículo recebido
    custo_total_usado = valor_proposto_usado + custo_recondicionamento_est
    margem_futura_usado = round(preco_fipe_usado - custo_total_usado, 2)

    # 3. Consolidação da Margem Combinada
    margem_combinada_reais = round(lucro_bruto_novo - overallowance + max(0.0, margem_futura_usado), 2)
    base_transacao = preco_venda_novo + preco_fipe_usado
    margem_combinada_pct = round((margem_combinada_reais / base_transacao) * 100, 2) if base_transacao > 0 else 0.0

    status_aprovacao = "APROVADO" if margem_combinada_pct >= 8.0 else "REQUER_ALCADA_GERENCIAL"
    requer_alcada = status_aprovacao == "REQUER_ALCADA_GERENCIAL"

    if status_aprovacao == "APROVADO":
        recomendacao = f"Operação aprovada com margem combinada de {margem_combinada_pct}% (R$ {margem_combinada_reais:,.2f})."
    else:
        recomendacao = f"Alerta de Margem: {margem_combinada_pct}% está abaixo do piso mínimo de 8.0%. Requer liberação do gerente."

    return {
        "veiculo_desejado": {
            "preco_venda": preco_venda_novo,
            "custo_aquisicao": custo_aquisicao_novo,
            "lucro_bruto_novo": lucro_bruto_novo
        },
        "usado_tradein": {
            "preco_fipe": preco_fipe_usado,
            "custo_recondicionamento_est": custo_recondicionamento_est,
            "oferta_minima": max(0.0, oferta_minima),
            "oferta_ideal_sugerida": max(0.0, oferta_ideal_sugerida),
            "oferta_maxima": max(0.0, oferta_maxima),
            "valor_proposto_usado": valor_proposto_usado,
            "overallowance": overallowance,
            "margem_futura_usado": margem_futura_usado
        },
        "analise_combinada": {
            "margem_combinada_reais": margem_combinada_reais,
            "margem_combinada_percentual": margem_combinada_pct,
            "status_aprovacao": status_aprovacao,
            "requer_alcada_gerente": requer_alcada,
            "recomendacao": recomendacao
        }
    }
