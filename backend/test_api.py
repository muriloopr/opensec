import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.main import app, http_client

client = TestClient(app)

def test_listar_veiculos(monkeypatch):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [
        {"id": 1, "marca": "Toyota", "modelo": "Corolla", "ano": 2022, "preco": 120000.0, "status": "disponivel", "loja_id": 1},
        {"id": 2, "marca": "Honda", "modelo": "Civic", "ano": 2021, "preco": 110000.0, "status": "vendido", "loja_id": 1}
    ]
    monkeypatch.setattr(http_client, "get", lambda url, **kwargs: mock_resp)

    response = client.get("/veiculos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_filtrar_veiculos_status(monkeypatch):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [
        {"id": 1, "marca": "Toyota", "modelo": "Corolla", "ano": 2022, "preco": 120000.0, "status": "disponivel", "loja_id": 1}
    ]
    monkeypatch.setattr(http_client, "get", lambda url, **kwargs: mock_resp)

    response = client.get("/veiculos?status=disponivel")
    assert response.status_code == 200
    data = response.json()
    for v in data:
        assert v["status"] == "disponivel"

def test_criar_veiculo_e_venda(monkeypatch):
    # Mock criação de veículo
    mock_veiculo_resp = MagicMock()
    mock_veiculo_resp.status_code = 201
    mock_veiculo_resp.json.return_value = {
        "id": 10,
        "marca": "Chevrolet",
        "modelo": "Onix",
        "ano": 2023,
        "preco": 75000.0,
        "status": "disponivel",
        "loja_id": 1
    }

    # Mock criação de venda
    mock_venda_resp = MagicMock()
    mock_venda_resp.status_code = 201
    mock_venda_resp.json.return_value = {
        "id": 5,
        "veiculo_id": 10,
        "cliente_id": 1,
        "vendedor_id": 2,
        "valor": 75000.0,
        "tipo_pagamento": "venda",
        "data": "2026-10-19"
    }

    def mock_post(url, **kwargs):
        if "/veiculo" in url:
            return mock_veiculo_resp
        elif "/venda" in url:
            return mock_venda_resp
        return MagicMock(status_code=404)

    monkeypatch.setattr(http_client, "post", mock_post)

    # 1. Criar veículo
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
    assert veiculo["id"] == 10

    # 2. Registrar venda
    payload_venda = {
        "veiculo_id": 10,
        "cliente_id": 1,
        "vendedor_id": 2,
        "valor": 75000.0,
        "tipo_pagamento": "venda"
    }
    r_venda = client.post("/vendas", json=payload_venda)
    assert r_venda.status_code == 201
    venda_data = r_venda.json()
    assert venda_data["veiculo_id"] == 10

def test_registrar_manutencao(monkeypatch):
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {
        "id": 8,
        "veiculo_id": 10,
        "mecanico_id": 3,
        "descricao": "Troca de óleo e revisão de freios",
        "custo": 450.0,
        "data_inicio": "2026-10-19"
    }
    monkeypatch.setattr(http_client, "post", lambda url, **kwargs: mock_resp)

    payload_m = {
        "veiculo_id": 10,
        "mecanico_id": 3,
        "descricao": "Troca de óleo e revisão de freios",
        "custo": 450.0
    }
    r_m = client.post("/manutencoes", json=payload_m)
    assert r_m.status_code == 201
    assert r_m.json()["veiculo_id"] == 10

def test_lojas_e_funcionarios():
    # Testar endpoints com fallback estático ou resposta simulada
    r_lojas = client.get("/lojas")
    assert r_lojas.status_code == 200
    assert len(r_lojas.json()) >= 2

    r_funcs = client.get("/funcionarios")
    assert r_funcs.status_code == 200
    assert len(r_funcs.json()) >= 3

def test_auth_signup_and_login(monkeypatch):
    signup_payload = {
        "email": "teste@concessionaria.com",
        "senha": "senha123"
    }

    mock_signup_resp = MagicMock()
    mock_signup_resp.status_code = 201
    mock_signup_resp.json.return_value = {
        "authToken": "fake-jwt-token-xyz",
        "user_id": 42
    }

    mock_login_resp = MagicMock()
    mock_login_resp.status_code = 200
    mock_login_resp.json.return_value = {
        "authToken": "fake-jwt-token-xyz",
        "user_id": 42
    }

    def mock_post(url, **kwargs):
        if "/auth/signup" in url:
            return mock_signup_resp
        elif "/auth/login" in url:
            return mock_login_resp
        return MagicMock(status_code=404)

    monkeypatch.setattr(http_client, "post", mock_post)

    # Signup
    r = client.post("/auth/signup", json=signup_payload)
    assert r.status_code == 201
    assert r.json()["id"] == 42
    assert r.json()["access_token"] == "fake-jwt-token-xyz"

    # Login
    r_login = client.post("/auth/login", json=signup_payload)
    assert r_login.status_code == 200
    data = r_login.json()
    assert data["access_token"] == "fake-jwt-token-xyz"
    assert data["email"] == signup_payload["email"]
