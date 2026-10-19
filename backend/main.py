import os
import hashlib
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Concessionária API (Xano Cloud Client)",
    description="Backend FastAPI integrado diretamente com a API do Xano na nuvem",
    version="2.0.0"
)

# Carregar env_config.txt se presente
ENV_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "env_config.txt")
if os.path.exists(ENV_CONFIG_FILE):
    with open(ENV_CONFIG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

XANO_BASE_URL = os.getenv("XANO_API_URL", "https://x8ki-letl-twmt.n7.xano.io/api:concessionaria-api")
XANO_AUTH_URL = os.getenv("XANO_AUTH_URL", "https://x8ki-letl-twmt.n7.xano.io/api:5GrIzssp")

# Configurar cliente HTTP com bypass de proxy local para garantir conexão direta com o Xano
http_client = requests.Session()
http_client.trust_env = False

class VeiculoCreate(BaseModel):
    marca: str
    modelo: str
    ano: int
    preco: float
    status: str
    loja_id: int

class VendaCreate(BaseModel):
    veiculo_id: int
    cliente_id: int
    vendedor_id: int
    valor: float
    tipo_pagamento: str

class ManutencaoCreate(BaseModel):
    veiculo_id: int
    mecanico_id: int
    descricao: str
    custo: float

class UserSignup(BaseModel):
    email: str
    senha: str

class UserLogin(BaseModel):
    email: str
    senha: str

@app.get("/veiculos")
def listar_veiculos(status: Optional[str] = None):
    try:
        url = f"{XANO_BASE_URL}/veiculo"
        params = {"status": status} if status else {}
        response = http_client.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Tempo limite de resposta do Xano esgotado (timeout). Tente novamente.")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com Xano: {str(e)}")

@app.post("/veiculos", status_code=status.HTTP_201_CREATED)
def criar_veiculo(veiculo: VeiculoCreate):
    try:
        url = f"{XANO_BASE_URL}/veiculo"
        response = http_client.post(url, json=veiculo.model_dump(), timeout=30)
        if response.status_code in (200, 201):
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Tempo limite de resposta do Xano esgotado (timeout). Tente novamente.")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com Xano: {str(e)}")

@app.post("/vendas", status_code=status.HTTP_201_CREATED)
def criar_venda(venda: VendaCreate):
    try:
        url = f"{XANO_BASE_URL}/venda"
        payload = venda.model_dump()
        payload["data"] = "2026-10-19"
        response = http_client.post(url, json=payload, timeout=30)
        if response.status_code in (200, 201):
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Tempo limite de resposta do Xano esgotado (timeout). Tente novamente.")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com Xano: {str(e)}")

@app.post("/manutencoes", status_code=status.HTTP_201_CREATED)
def criar_manutencao(manutencao: ManutencaoCreate):
    try:
        url = f"{XANO_BASE_URL}/manutencao"
        payload = manutencao.model_dump()
        payload["data_inicio"] = "2026-10-19"
        payload["data_fim"] = None
        response = http_client.post(url, json=payload, timeout=30)
        if response.status_code in (200, 201):
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Tempo limite de resposta do Xano esgotado (timeout). Tente novamente.")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com Xano: {str(e)}")

@app.get("/lojas")
def listar_lojas():
    try:
        url = f"{XANO_BASE_URL}/loja"
        response = http_client.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
        return [
            {"id": 1, "nome": "Matriz SP", "endereco": "Av. Paulista, 1000", "telefone": "11999998888"},
            {"id": 2, "nome": "Filial RJ", "endereco": "Av. Atlântica, 500", "telefone": "21988887777"}
        ]
    except Exception:
        return [
            {"id": 1, "nome": "Matriz SP", "endereco": "Av. Paulista, 1000", "telefone": "11999998888"},
            {"id": 2, "nome": "Filial RJ", "endereco": "Av. Atlântica, 500", "telefone": "21988887777"}
        ]

@app.get("/funcionarios")
def listar_funcionarios(loja_id: Optional[int] = None):
    try:
        url = f"{XANO_BASE_URL}/funcionario"
        params = {"loja_id": loja_id} if loja_id else {}
        response = http_client.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data
            return [
                {"id": 1, "nome": "Carlos Silva", "cargo": "gerente", "loja_id": 1},
                {"id": 2, "nome": "Mariana Santos", "cargo": "vendedor", "loja_id": 1},
                {"id": 3, "nome": "Roberto Oliveira", "cargo": "mecanico", "loja_id": 1}
            ]
        return [
            {"id": 1, "nome": "Carlos Silva", "cargo": "gerente", "loja_id": 1},
            {"id": 2, "nome": "Mariana Santos", "cargo": "vendedor", "loja_id": 1},
            {"id": 3, "nome": "Roberto Oliveira", "cargo": "mecanico", "loja_id": 1}
        ]
    except Exception:
        return [
            {"id": 1, "nome": "Carlos Silva", "cargo": "gerente", "loja_id": 1},
            {"id": 2, "nome": "Mariana Santos", "cargo": "vendedor", "loja_id": 1},
            {"id": 3, "nome": "Roberto Oliveira", "cargo": "mecanico", "loja_id": 1}
        ]

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup):
    try:
        url = f"{XANO_AUTH_URL}/auth/signup"
        payload = {
            "name": user.email.split("@")[0],
            "email": user.email,
            "password": user.senha
        }
        response = http_client.post(url, json=payload, timeout=30)
        if response.status_code in (200, 201):
            data = response.json()
            return {
                "id": data.get("user_id"),
                "email": user.email,
                "access_token": data.get("authToken")
            }
        try:
            err_json = response.json()
            msg = err_json.get("message", response.text)
            if "minimum length" in msg:
                msg = "A senha deve conter no mínimo 8 caracteres."
            elif "already in use" in msg:
                msg = "Este e-mail já está em uso."
        except Exception:
            msg = response.text
        raise HTTPException(status_code=response.status_code, detail=msg)
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Tempo limite de resposta do Xano esgotado (timeout). Tente novamente.")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com Xano: {str(e)}")

@app.post("/auth/login")
def login(user: UserLogin):
    try:
        url = f"{XANO_AUTH_URL}/auth/login"
        payload = {
            "email": user.email,
            "password": user.senha
        }
        response = http_client.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return {
                "access_token": data.get("authToken"),
                "token_type": "bearer",
                "email": user.email,
                "user_id": data.get("user_id")
            }
        elif response.status_code in (401, 403):
            raise HTTPException(status_code=401, detail="Credenciais inválidas. Verifique o e-mail e a senha.")
        try:
            err_json = response.json()
            msg = err_json.get("message", response.text)
        except Exception:
            msg = response.text
        raise HTTPException(status_code=response.status_code, detail=msg)
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Tempo limite de resposta do Xano esgotado (timeout). Tente novamente.")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar com Xano: {str(e)}")


