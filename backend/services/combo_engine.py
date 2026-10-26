from typing import Dict, Any

def calcular_parcela_price(saldo_devedor: float, taxa_mensal: float, meses: int) -> float:
    """Calcula a parcela mensal fixa pelo Sistema de Amortização Francês (Tabela Price)."""
    if saldo_devedor <= 0 or meses <= 0:
        return 0.0
    if taxa_mensal <= 0:
        return round(saldo_devedor / meses, 2)
    fator = (1.0 + taxa_mensal) ** meses
    pmt = saldo_devedor * (taxa_mensal * fator) / (fator - 1.0)
    return round(pmt, 2)

def simular_combo_financiamento(
    preco_veiculo: float,
    valor_entrada: float,
    num_parcelas: int,
    taxa_juros_mensal: float,
    preco_pacote_manutencao: float,
    nome_pacote: str
) -> Dict[str, Any]:
    """
    Simula o financiamento comparando o formato tradicional vs. combo com manutenção embutida.
    """
    # 1. Simulação Tradicional (apenas saldo do veículo)
    saldo_tradicional = max(0.0, round(preco_veiculo - valor_entrada, 2))
    pmt_tradicional = calcular_parcela_price(saldo_tradicional, taxa_juros_mensal, num_parcelas)
    total_pago_tradicional = round(pmt_tradicional * num_parcelas, 2)
    total_juros_tradicional = round(max(0.0, total_pago_tradicional - saldo_tradicional), 2)

    # 2. Simulação Combo (veículo + pacote de manutenção preventiva)
    saldo_combo = round(saldo_tradicional + preco_pacote_manutencao, 2)
    pmt_combo = calcular_parcela_price(saldo_combo, taxa_juros_mensal, num_parcelas)
    total_pago_combo = round(pmt_combo * num_parcelas, 2)
    total_juros_combo = round(max(0.0, total_pago_combo - saldo_combo), 2)

    # Métricas de valor agregado e vendas
    diferenca_mensal = round(pmt_combo - pmt_tradicional, 2)
    economia_cliente = round(preco_pacote_manutencao * 0.30, 2) # ~30% de economia vs tabela avulsa
    comissao_loja_extra = round(preco_pacote_manutencao * 0.015, 2) # Retorno de intermediação bancária (1.5%)

    pitch = (
        f"Por apenas +R$ {diferenca_mensal:,.2f}/mês na sua parcela, garanta o {nome_pacote} "
        f"com economia estimada de R$ {economia_cliente:,.2f} em revisões e serviços oficiais."
    )

    return {
        "veiculo_preco": preco_veiculo,
        "valor_entrada": valor_entrada,
        "num_parcelas": num_parcelas,
        "taxa_juros_mensal": taxa_juros_mensal,
        "simulacao_tradicional": {
            "saldo_financiado": saldo_tradicional,
            "parcela_mensal": pmt_tradicional,
            "total_pago": total_pago_tradicional,
            "total_juros": total_juros_tradicional
        },
        "simulacao_combo": {
            "pacote_nome": nome_pacote,
            "pacote_valor": preco_pacote_manutencao,
            "saldo_financiado": saldo_combo,
            "parcela_mensal": pmt_combo,
            "total_pago": total_pago_combo,
            "total_juros": total_juros_combo,
            "diferenca_parcela_mensal": diferenca_mensal,
            "economia_cliente_estimada": economia_cliente,
            "comissao_adicional_loja": comissao_loja_extra,
            "pitch_venda": pitch
        }
    }
