import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from backend.main import app, DB_FILE, init_db, get_db
from backend.services.pricing_engine import calcular_custo_patio_veiculo
from backend.services.tradein_engine import calcular_tradein_margem_combinada
from backend.services.combo_engine import calcular_parcela_price, simular_combo_financiamento

client = TestClient(app)

# ==================== Testes Unitários de Serviços ====================

def test_pricing_engine_faixas_aging():
    agora = datetime.now()
    
    # 1. Menos de 30 dias (Normal)
    dt_10_dias = (agora - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
    res_normal = calcular_custo_patio_veiculo(
        custo_aquisicao=100000.0,
        preco_atual=120000.0,
        data_entrada_str=dt_10_dias
    )
    assert res_normal["dias_em_estoque"] >= 9
    assert res_normal["status_aging"] == "NORMAL"
    assert res_normal["desconto_sugerido"] == 0.0
    assert res_normal["novo_preco_sugerido"] == 120000.0

    # 2. Entre 31 e 45 dias (Alerta Amarelo)
    dt_35_dias = (agora - timedelta(days=35)).strftime("%Y-%m-%d %H:%M:%S")
    res_amarelo = calcular_custo_patio_veiculo(
        custo_aquisicao=100000.0,
        preco_atual=120000.0,
        data_entrada_str=dt_35_dias
    )
    assert res_amarelo["status_aging"] == "ALERTA_AMARELO"
    assert res_amarelo["desconto_sugerido"] > 0
    assert res_amarelo["novo_preco_sugerido"] < 120000.0

    # 3. Mais de 45 dias (Alerta Vermelho)
    dt_50_dias = (agora - timedelta(days=50)).strftime("%Y-%m-%d %H:%M:%S")
    res_vermelho = calcular_custo_patio_veiculo(
        custo_aquisicao=100000.0,
        preco_atual=120000.0,
        data_entrada_str=dt_50_dias
    )
    assert res_vermelho["status_aging"] == "ALERTA_VERMELHO"
    assert res_vermelho["desconto_sugerido"] > 0
    # Verifica respeito ao piso de segurança (custo * 1.02 = 102000.0)
    assert res_vermelho["novo_preco_sugerido"] >= 102000.0


def test_tradein_engine_aprovado_e_bloqueado():
    # Caso 1: Negociação Saudável (Margem combinada >= 8%)
    res_aprovado = calcular_tradein_margem_combinada(
        preco_venda_novo=120000.0,
        custo_aquisicao_novo=100000.0,     # Lucro novo = 20.000
        preco_fipe_usado=70000.0,
        custo_recondicionamento_est=2000.0,
        valor_proposto_usado=55000.0        # Oferta conservadora
    )
    assert res_aprovado["analise_combinada"]["status_aprovacao"] == "APROVADO"
    assert res_aprovado["analise_combinada"]["requer_alcada_gerente"] is False
    assert res_aprovado["analise_combinada"]["margem_combinada_percentual"] >= 8.0

    # Caso 2: Negociação com Overallowance excessivo (Margem combinada < 8%)
    res_bloqueado = calcular_tradein_margem_combinada(
        preco_venda_novo=105000.0,
        custo_aquisicao_novo=100000.0,     # Lucro novo baixo = 5.000
        preco_fipe_usado=50000.0,
        custo_recondicionamento_est=4000.0,
        valor_proposto_usado=52000.0        # Paga mais que a FIPE
    )
    assert res_bloqueado["analise_combinada"]["status_aprovacao"] == "REQUER_ALCADA_GERENCIAL"
    assert res_bloqueado["analise_combinada"]["requer_alcada_gerente"] is True
    assert res_bloqueado["analise_combinada"]["margem_combinada_percentual"] < 8.0


def test_combo_engine_price_e_simulacao():
    pmt = calcular_parcela_price(saldo_devedor=60000.0, taxa_mensal=0.015, meses=48)
    assert pmt > 1250.0 and pmt < 2000.0

    sim = simular_combo_financiamento(
        preco_veiculo=100000.0,
        valor_entrada=30000.0,
        num_parcelas=48,
        taxa_juros_mensal=0.0169,
        preco_pacote_manutencao=3200.0,
        nome_pacote="Plano Prata"
    )
    assert sim["simulacao_tradicional"]["saldo_financiado"] == 70000.0
    assert sim["simulacao_combo"]["saldo_financiado"] == 73200.0
    assert sim["simulacao_combo"]["diferenca_parcela_mensal"] > 0
    assert sim["simulacao_combo"]["economia_cliente_estimada"] > 0
    assert "pitch_venda" in sim["simulacao_combo"]


# ==================== Testes de Integração com a API ====================

def test_api_dashboard_precificacao():
    r = client.get("/precificacao/patio/dashboard")
    assert r.status_code == 200
    data = r.json()
    assert "total_veiculos_patio" in data
    assert "custo_total_carregamento_dia" in data
    assert "itens" in data
    assert len(data["itens"]) >= 1

    # Testa aplicação de reajuste sugerido
    primeiro_veiculo = data["itens"][0]
    vid = primeiro_veiculo["veiculo_id"]
    preco_antigo = primeiro_veiculo["preco_atual"]
    novo_preco = round(preco_antigo * 0.95, 2)

    r_reajuste = client.post(
        f"/precificacao/veiculos/{vid}/aplicar-reajuste",
        json={"novo_preco": novo_preco, "motivo": "Teste automatizado"}
    )
    assert r_reajuste.status_code == 200
    res_json = r_reajuste.json()
    assert res_json["preco_novo"] == novo_preco


def test_api_tradein_fluxo_completo():
    # 1. Buscar veículos disponíveis
    r_v = client.get("/veiculos?status=disponivel")
    veiculos = r_v.json()
    assert len(veiculos) > 0
    vid = veiculos[0]["id"]

    # 2. Avaliar Trade-In
    payload_aval = {
        "veiculo_desejado_id": vid,
        "cliente_id": 1,
        "vendedor_id": 2,
        "marca_usado": "Volkswagen",
        "modelo_usado": "Fox",
        "ano_usado": 2019,
        "km_usado": 60000,
        "preco_fipe": 45000.0,
        "custo_recondicionamento_est": 1500.0,
        "valor_proposto_usado": 36000.0
    }
    r_aval = client.post("/tradein/avaliar", json=payload_aval)
    assert r_aval.status_code == 200
    data_aval = r_aval.json()
    assert "analise_combinada" in data_aval
    assert "margem_combinada_reais" in data_aval["analise_combinada"]

    # 3. Salvar Avaliação
    payload_salvar = {
        "veiculo_desejado_id": vid,
        "cliente_id": 1,
        "vendedor_id": 2,
        "marca_usado": "Volkswagen",
        "modelo_usado": "Fox",
        "ano_usado": 2019,
        "km_usado": 60000,
        "preco_fipe": 45000.0,
        "custo_recondicionamento_est": 1500.0,
        "oferta_ideal_sugerida": data_aval["usado_tradein"]["oferta_ideal_sugerida"],
        "valor_proposto_usado": 36000.0,
        "overallowance": data_aval["usado_tradein"]["overallowance"],
        "lucro_veiculo_novo": data_aval["veiculo_desejado"]["lucro_bruto_novo"],
        "margem_futura_usado": data_aval["usado_tradein"]["margem_futura_usado"],
        "margem_combinada_reais": data_aval["analise_combinada"]["margem_combinada_reais"],
        "margem_combinada_percentual": data_aval["analise_combinada"]["margem_combinada_percentual"],
        "status": "aprovado"
    }
    r_salvar = client.post("/tradein/salvar", json=payload_salvar)
    assert r_salvar.status_code == 201
    tradein_id = r_salvar.json()["id"]

    # 4. Listar Histórico
    r_hist = client.get("/tradein/historico")
    assert r_hist.status_code == 200
    assert any(h["id"] == tradein_id for h in r_hist.json())


def test_api_combos_e_venda_integrada():
    # 1. Listar pacotes
    r_pacotes = client.get("/combos/pacotes")
    assert r_pacotes.status_code == 200
    pacotes = r_pacotes.json()
    assert len(pacotes) >= 2
    pacote_id = pacotes[0]["id"]

    # 2. Criar veículo para venda
    r_v = client.post("/veiculos", json={
        "marca": "Hyundai",
        "modelo": "HB20",
        "ano": 2023,
        "preco": 72000.0,
        "custo_aquisicao": 60000.0,
        "status": "disponivel",
        "loja_id": 1
    })
    assert r_v.status_code == 201
    veiculo_id = r_v.json()["id"]

    # 3. Simular financiamento com combo
    r_sim = client.post("/combos/simular-financiamento", json={
        "veiculo_id": veiculo_id,
        "valor_entrada": 20000.0,
        "num_parcelas": 48,
        "taxa_juros_mensal": 0.0169,
        "pacote_manutencao_id": pacote_id
    })
    assert r_sim.status_code == 200
    sim_data = r_sim.json()
    assert sim_data["simulacao_combo"]["diferenca_parcela_mensal"] > 0

    # 4. Efetuar venda vinculando combo
    r_venda = client.post("/vendas", json={
        "veiculo_id": veiculo_id,
        "cliente_id": 1,
        "vendedor_id": 2,
        "valor": 72000.0,
        "tipo_pagamento": "financiamento",
        "pacote_manutencao_id": pacote_id
    })
    assert r_venda.status_code == 201
    venda = r_venda.json()
    assert venda["veiculo_id"] == veiculo_id
    assert venda["pacote_manutencao_id"] == pacote_id
    assert venda["lucro_combinado"] > 0
