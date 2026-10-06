import sqlite3
import hashlib
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Concessionária API (FastAPI + XanoScript Model)",
    description="Backend FastAPI simulando/integrando com o modelo de dados XanoScript",
    version="1.0.0"
)

DB_FILE = "concessionaria.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loja (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        endereco TEXT,
        telefone TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cargo TEXT NOT NULL,
        loja_id INTEGER,
        FOREIGN KEY(loja_id) REFERENCES loja(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        ano INTEGER NOT NULL,
        preco REAL NOT NULL,
        status TEXT NOT NULL,
        loja_id INTEGER,
        FOREIGN KEY(loja_id) REFERENCES loja(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        celular TEXT,
        cpf TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS venda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        veiculo_id INTEGER,
        cliente_id INTEGER,
        vendedor_id INTEGER,
        data TEXT,
        valor REAL,
        tipo_pagamento TEXT,
        FOREIGN KEY(veiculo_id) REFERENCES veiculo(id),
        FOREIGN KEY(cliente_id) REFERENCES cliente(id),
        FOREIGN KEY(vendedor_id) REFERENCES funcionario(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS manutencao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        veiculo_id INTEGER,
        mecanico_id INTEGER,
        data_inicio TEXT,
        data_fim TEXT,
        descricao TEXT,
        custo REAL,
        FOREIGN KEY(veiculo_id) REFERENCES veiculo(id),
        FOREIGN KEY(mecanico_id) REFERENCES funcionario(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilizador (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    
    # Inserir dados iniciais se vazio
    cursor.execute("SELECT COUNT(*) FROM loja")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO loja (nome, endereco, telefone) VALUES ('Matriz SP', 'Av. Paulista, 1000', '11999998888')")
        cursor.execute("INSERT INTO loja (nome, endereco, telefone) VALUES ('Filial RJ', 'Av. Atlântica, 500', '21988887777')")
        cursor.execute("INSERT INTO funcionario (nome, cargo, loja_id) VALUES ('Carlos Silva', 'gerente', 1)")
        cursor.execute("INSERT INTO funcionario (nome, cargo, loja_id) VALUES ('Ana Souza', 'vendedor', 1)")
        cursor.execute("INSERT INTO funcionario (nome, cargo, loja_id) VALUES ('João Mecânico', 'mecanico', 1)")
        cursor.execute("INSERT INTO veiculo (marca, modelo, ano, preco, status, loja_id) VALUES ('Toyota', 'Corolla', 2023, 120000.0, 'disponivel', 1)")
        cursor.execute("INSERT INTO veiculo (marca, modelo, ano, preco, status, loja_id) VALUES ('Honda', 'Civic', 2022, 110000.0, 'disponivel', 1)")
        cursor.execute("INSERT INTO cliente (celular, cpf) VALUES ('11977776666', '12345678901')")
        conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Pydantic models
class LojaCreate(BaseModel):
    nome: str
    endereco: Optional[str] = None
    telefone: Optional[str] = None

class FuncionarioCreate(BaseModel):
    nome: str
    cargo: str
    loja_id: int

class VeiculoCreate(BaseModel):
    marca: str
    modelo: str
    ano: int
    preco: float
    status: str = "disponivel"
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

@app.get("/veiculos")
def listar_veiculos(status: Optional[str] = None):
    conn = get_db()
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM veiculo WHERE status = ?", (status,))
    else:
        cursor.execute("SELECT * FROM veiculo")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

@app.post("/veiculos", status_code=status.HTTP_201_CREATED)
def criar_veiculo(veiculo: VeiculoCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO veiculo (marca, modelo, ano, preco, status, loja_id) VALUES (?, ?, ?, ?, ?, ?)",
        (veiculo.marca, veiculo.modelo, veiculo.ano, veiculo.preco, veiculo.status, veiculo.loja_id)
    )
    conn.commit()
    vid = cursor.lastrowid
    cursor.execute("SELECT * FROM veiculo WHERE id = ?", (vid,))
    row = dict(cursor.fetchone())
    conn.close()
    return row

@app.post("/vendas", status_code=status.HTTP_201_CREATED)
def registrar_venda(venda: VendaCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT status FROM veiculo WHERE id = ?", (venda.veiculo_id,))
    v = cursor.fetchone()
    if not v:
        conn.close()
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    if v["status"] != "disponivel":
        conn.close()
        raise HTTPException(status_code=400, detail="Veículo não está disponível para venda")
        
    cursor.execute(
        "INSERT INTO venda (veiculo_id, cliente_id, vendedor_id, data, valor, tipo_pagamento) VALUES (?, ?, ?, datetime('now'), ?, ?)",
        (venda.veiculo_id, venda.cliente_id, venda.vendedor_id, venda.valor, venda.tipo_pagamento)
    )
    cursor.execute("UPDATE veiculo SET status = 'vendido' WHERE id = ?", (venda.veiculo_id,))
    conn.commit()
    vid = cursor.lastrowid
    cursor.execute("SELECT * FROM venda WHERE id = ?", (vid,))
    row = dict(cursor.fetchone())
    conn.close()
    return row

@app.post("/manutencoes", status_code=status.HTTP_201_CREATED)
def registrar_manutencao(m: ManutencaoCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO manutencao (veiculo_id, mecanico_id, data_inicio, descricao, custo) VALUES (?, ?, datetime('now'), ?, ?)",
        (m.veiculo_id, m.mecanico_id, m.descricao, m.custo)
    )
    cursor.execute("UPDATE veiculo SET status = 'em_manutencao' WHERE id = ?", (m.veiculo_id,))
    conn.commit()
    mid = cursor.lastrowid
    cursor.execute("SELECT * FROM manutencao WHERE id = ?", (mid,))
    row = dict(cursor.fetchone())
    conn.close()
    return row

@app.get("/funcionarios")
def listar_funcionarios(loja_id: Optional[int] = None):
    conn = get_db()
    cursor = conn.cursor()
    if loja_id:
        cursor.execute("SELECT * FROM funcionario WHERE loja_id = ?", (loja_id,))
    else:
        cursor.execute("SELECT * FROM funcionario")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

@app.get("/lojas")
def listar_lojas():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM loja")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

class UserSignup(BaseModel):
    email: str
    senha: str

class UserLogin(BaseModel):
    email: str
    senha: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM utilizador WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    senha_hash = hash_password(user.senha)
    cursor.execute("INSERT INTO utilizador (email, senha_hash) VALUES (?, ?)", (user.email, senha_hash))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return {"id": user_id, "email": user.email, "message": "Utilizador cadastrado com sucesso"}

@app.post("/auth/login")
def login(user: UserLogin):
    conn = get_db()
    cursor = conn.cursor()
    senha_hash = hash_password(user.senha)
    cursor.execute("SELECT id, email FROM utilizador WHERE email = ? AND senha_hash = ?", (user.email, senha_hash))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = f"token-jwt-{row['id']}-{row['email']}"
    return {"access_token": token, "token_type": "bearer", "email": row['email']}
