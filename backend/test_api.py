import os
import pytest
from fastapi.testclient import TestClient
from backend.main import app, DB_FILE, init_db

# Remover banco de teste antigo e reinicializar
if os.path.exists(DB_FILE):
    try:
        os.remove(DB_FILE)
    except:
        pass

init_db()

client = TestClient(app)

def test_listar_veiculos():
    response = client.get("/veiculos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_filtrar_veiculos_status():
    response = client.get("/veiculos?status=disponivel")
    assert response.status_code == 200
    data = response.json()
    for v in data:
        assert v["status"] == "disponivel"

def test_criar_veiculo_e_venda():
    # Criar veiculo novo
    payload_veiculo = {
        "marca": "Chevrolet",
        "modelo": "Onix",
        "ano": 2023,
        "preco": 75000.0,
        "status": "disponivel",
        "loja_id": 1
    }
    r = client.post("/veiculos", json=payload_veiculo)
    assert r.status_code == 201
    veiculo = r.json()
    v_id = veiculo["id"]
    assert veiculo["status"] == "disponivel"

    # Registrar venda do veiculo disponivel
    payload_venda = {
        "veiculo_id": v_id,
        "cliente_id": 1,
        "vendedor_id": 2,
        "valor": 75000.0,
        "tipo_pagamento": "venda"
    }
    r_venda = client.post("/vendas", json=payload_venda)
    assert r_venda.status_code == 201
    venda_data = r_venda.json()
    assert venda_data["veiculo_id"] == v_id

    # Tentar vender o mesmo veiculo novamente (deve falhar pois status agora é 'vendido')
    r_venda_2 = client.post("/vendas", json=payload_venda)
    assert r_venda_2.status_code == 400

def test_registrar_manutencao():
    # Criar outro veiculo
    payload_veiculo = {
        "marca": "Fiat",
        "modelo": "Argo",
        "ano": 2021,
        "preco": 60000.0,
        "status": "disponivel",
        "loja_id": 1
    }
    r = client.post("/veiculos", json=payload_veiculo)
    assert r.status_code == 201
    v_id = r.json()["id"]

    # Registrar manutencao
    payload_m = {
        "veiculo_id": v_id,
        "mecanico_id": 3,
        "descricao": "Troca de óleo e revisão de freios",
        "custo": 450.0
    }
    r_m = client.post("/manutencoes", json=payload_m)
    assert r_m.status_code == 201
    manut_data = r_m.json()
    assert manut_data["veiculo_id"] == v_id

    # Verificar se status mudou para em_manutencao
    r_v = client.get(f"/veiculos")
    veiculos = r_v.json()
    veiculo_atualizado = next(v for v in veiculos if v["id"] == v_id)
    assert veiculo_atualizado["status"] == "em_manutencao"

def test_lojas_e_funcionarios():
    r_lojas = client.get("/lojas")
    assert r_lojas.status_code == 200
    assert len(r_lojas.json()) >= 2

    r_funcs = client.get("/funcionarios")
    assert r_funcs.status_code == 200
    assert len(r_funcs.json()) >= 3

def test_auth_signup_and_login():
    signup_payload = {
        "email": "teste@concessionaria.com",
        "senha": "senha123"
    }
    # Signup
    r = client.post("/auth/signup", json=signup_payload)
    assert r.status_code == 201
    assert "id" in r.json()

    # Signup duplicado deve falhar
    r_dup = client.post("/auth/signup", json=signup_payload)
    assert r_dup.status_code == 400

    # Login com sucesso
    r_login = client.post("/auth/login", json=signup_payload)
    assert r_login.status_code == 200
    data = r_login.json()
    assert "access_token" in data
    assert data["email"] == signup_payload["email"]

    # Login com senha incorreta deve falhar
    r_wrong = client.post("/auth/login", json={"email": "teste@concessionaria.com", "senha": "errada"})
    assert r_wrong.status_code == 401
