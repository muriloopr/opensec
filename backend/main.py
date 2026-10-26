import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from backend.services.pricing_engine import calcular_custo_patio_veiculo
from backend.services.tradein_engine import calcular_tradein_margem_combinada
from backend.services.combo_engine import simular_combo_financiamento

app = FastAPI(
    title="Concessionária API (FastAPI + XanoScript Model)",
    description="Backend FastAPI com Motor de Precificação Dinâmica, Avaliador de Trade-In e Simulador de Combos",
    version="1.1.0"
)

DB_FILE = "concessionaria.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Tabelas existentes
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
        custo_aquisicao REAL NOT NULL DEFAULT 0.0,
        preco_original REAL DEFAULT 0.0,
        data_entrada TEXT DEFAULT (datetime('now')),
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
        tradein_id INTEGER NULL,
        pacote_manutencao_id INTEGER NULL,
        lucro_combinado REAL DEFAULT 0.0,
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
    
    # 2. Novas tabelas do Motor de Precificação e Trade-In
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS custo_patio_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        taxa_custo_capital_anual REAL NOT NULL DEFAULT 0.12,
        taxa_depreciacao_anual REAL NOT NULL DEFAULT 0.15,
        taxa_seguro_anual REAL NOT NULL DEFAULT 0.012,
        dias_gatilho_alerta INTEGER NOT NULL DEFAULT 30,
        atualizado_em TEXT DEFAULT (datetime('now'))
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacao_tradein (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        veiculo_desejado_id INTEGER NOT NULL,
        vendedor_id INTEGER NOT NULL,
        marca_usado TEXT NOT NULL,
        modelo_usado TEXT NOT NULL,
        ano_usado INTEGER NOT NULL,
        km_usado INTEGER NOT NULL,
        preco_fipe REAL NOT NULL,
        custo_recondicionamento_est REAL NOT NULL DEFAULT 0.0,
        oferta_ideal_sugerida REAL NOT NULL,
        valor_proposto_usado REAL NOT NULL,
        overallowance REAL NOT NULL DEFAULT 0.0,
        lucro_veiculo_novo REAL NOT NULL,
        margem_futura_usado REAL NOT NULL,
        margem_combinada_reais REAL NOT NULL,
        margem_combinada_percentual REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'em_analise',
        criado_em TEXT DEFAULT (datetime('now')),
        FOREIGN KEY(cliente_id) REFERENCES cliente(id),
        FOREIGN KEY(veiculo_desejado_id) REFERENCES veiculo(id),
        FOREIGN KEY(vendedor_id) REFERENCES funcionario(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacote_manutencao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        duracao_meses INTEGER NOT NULL,
        qtd_revisoes INTEGER NOT NULL,
        preco_tabela REAL NOT NULL,
        custo_estimado REAL NOT NULL,
        descricao TEXT,
        ativo INTEGER NOT NULL DEFAULT 1
    )
    """)

    # 3. Migrações dinâmicas para colunas em tabelas existentes
    def add_col(tabela, col_def):
        col_name = col_def.split()[0]
        cursor.execute(f"PRAGMA table_info({tabela})")
        cols = [c[1] for c in cursor.fetchall()]
        if col_name not in cols:
            cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {col_def}")

    add_col("veiculo", "custo_aquisicao REAL DEFAULT 0.0")
    add_col("veiculo", "preco_original REAL DEFAULT 0.0")
    add_col("veiculo", "data_entrada TEXT DEFAULT ''")
    add_col("venda", "tradein_id INTEGER NULL")
    add_col("venda", "pacote_manutencao_id INTEGER NULL")
    add_col("venda", "lucro_combinado REAL DEFAULT 0.0")

    cursor.execute("UPDATE veiculo SET data_entrada = datetime('now') WHERE data_entrada IS NULL OR data_entrada = ''")
    conn.commit()

    # 4. Dados Iniciais (Seed)
    cursor.execute("SELECT COUNT(*) FROM loja")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO loja (nome, endereco, telefone) VALUES ('Matriz SP', 'Av. Paulista, 1000', '11999998888')")
        cursor.execute("INSERT INTO loja (nome, endereco, telefone) VALUES ('Filial RJ', 'Av. Atlântica, 500', '21988887777')")
        cursor.execute("INSERT INTO funcionario (nome, cargo, loja_id) VALUES ('Carlos Silva', 'gerente', 1)")
        cursor.execute("INSERT INTO funcionario (nome, cargo, loja_id) VALUES ('Ana Souza', 'vendedor', 1)")
        cursor.execute("INSERT INTO funcionario (nome, cargo, loja_id) VALUES ('João Mecânico', 'mecanico', 1)")
        
        agora = datetime.now()
        data_48_dias = (agora - timedelta(days=48)).strftime("%Y-%m-%d %H:%M:%S")
        data_36_dias = (agora - timedelta(days=36)).strftime("%Y-%m-%d %H:%M:%S")
        data_12_dias = (agora - timedelta(days=12)).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO veiculo (marca, modelo, ano, preco, custo_aquisicao, preco_original, data_entrada, status, loja_id) "
            "VALUES ('Toyota', 'Corolla', 2023, 120000.0, 102000.0, 120000.0, ?, 'disponivel', 1)",
            (data_48_dias,)
        )
        cursor.execute(
            "INSERT INTO veiculo (marca, modelo, ano, preco, custo_aquisicao, preco_original, data_entrada, status, loja_id) "
            "VALUES ('Honda', 'Civic', 2022, 110000.0, 95000.0, 110000.0, ?, 'disponivel', 1)",
            (data_36_dias,)
        )
        cursor.execute(
            "INSERT INTO veiculo (marca, modelo, ano, preco, custo_aquisicao, preco_original, data_entrada, status, loja_id) "
            "VALUES ('Jeep', 'Compass', 2024, 155000.0, 135000.0, 155000.0, ?, 'disponivel', 1)",
            (data_12_dias,)
        )
        cursor.execute("INSERT INTO cliente (celular, cpf) VALUES ('11977776666', '12345678901')")
        conn.commit()

    # Seed de custo de pátio config
    cursor.execute("SELECT COUNT(*) FROM custo_patio_config")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO custo_patio_config (taxa_custo_capital_anual, taxa_depreciacao_anual, taxa_seguro_anual, dias_gatilho_alerta) "
            "VALUES (0.12, 0.15, 0.012, 30)"
        )
        conn.commit()

    # Seed de pacotes de manutenção
    cursor.execute("SELECT COUNT(*) FROM pacote_manutencao")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO pacote_manutencao (nome, duracao_meses, qtd_revisoes, preco_tabela, custo_estimado, descricao)
        VALUES 
        ('Plano Bronze - 1 Ano de Revisão', 12, 2, 1800.0, 1000.0, 'Troca de óleo, filtros e inspeção técnica de 50 itens aos 10.000km e 20.000km'),
        ('Plano Prata - 2 Anos de Revisão Garantida', 24, 4, 3200.0, 1800.0, '4 revisões completas com peças originais + alinhamento, balanceamento e rodízio'),
        ('Plano Ouro - 2 Anos + Garantia Estendida', 24, 4, 4800.0, 2600.0, '4 revisões completas + garantia estendida de trem de força por 24 meses')
        """)
        conn.commit()

    # Garantir que veículos existentes com custo_aquisicao = 0 sejam atualizados com uma estimativa razoável
    cursor.execute("UPDATE veiculo SET custo_aquisicao = round(preco * 0.85, 2) WHERE custo_aquisicao <= 0")
    cursor.execute("UPDATE veiculo SET preco_original = preco WHERE preco_original IS NULL OR preco_original <= 0")
    conn.commit()

    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# ==================== Pydantic Models ====================

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
    custo_aquisicao: Optional[float] = None
    data_entrada: Optional[str] = None
    status: str = "disponivel"
    loja_id: int

class VendaCreate(BaseModel):
    veiculo_id: int
    cliente_id: int
    vendedor_id: int
    valor: float
    tipo_pagamento: str
    tradein_id: Optional[int] = None
    pacote_manutencao_id: Optional[int] = None

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

class ReajustePrecoRequest(BaseModel):
    novo_preco: float
    motivo: Optional[str] = "Reajuste dinâmico por aging de pátio"

class TradeInAvaliacaoRequest(BaseModel):
    veiculo_desejado_id: int
    cliente_id: Optional[int] = None
    vendedor_id: Optional[int] = 1
    marca_usado: str
    modelo_usado: str
    ano_usado: int
    km_usado: int
    preco_fipe: float
    custo_recondicionamento_est: float = 0.0
    valor_proposto_usado: float
    margem_alvo_revenda: Optional[float] = 0.15

class TradeInSalvarRequest(BaseModel):
    veiculo_desejado_id: int
    cliente_id: Optional[int] = None
    vendedor_id: int = 1
    marca_usado: str
    modelo_usado: str
    ano_usado: int
    km_usado: int
    preco_fipe: float
    custo_recondicionamento_est: float = 0.0
    oferta_ideal_sugerida: float
    valor_proposto_usado: float
    overallowance: float = 0.0
    lucro_veiculo_novo: float
    margem_futura_usado: float
    margem_combinada_reais: float
    margem_combinada_percentual: float
    status: str = "aprovado"

class SimuladorComboRequest(BaseModel):
    veiculo_id: int
    valor_entrada: float = 0.0
    num_parcelas: int = 48
    taxa_juros_mensal: float = 0.0169
    pacote_manutencao_id: Optional[int] = None

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ==================== Endpoints: Veículos ====================

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

@app.get("/veiculos/{veiculo_id}")
def obter_veiculo(veiculo_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM veiculo WHERE id = ?", (veiculo_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return dict(row)

@app.post("/veiculos", status_code=status.HTTP_201_CREATED)
def criar_veiculo(veiculo: VeiculoCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    custo = veiculo.custo_aquisicao if veiculo.custo_aquisicao and veiculo.custo_aquisicao > 0 else round(veiculo.preco * 0.85, 2)
    data_ent = veiculo.data_entrada if veiculo.data_entrada else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO veiculo (marca, modelo, ano, preco, custo_aquisicao, preco_original, data_entrada, status, loja_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (veiculo.marca, veiculo.modelo, veiculo.ano, veiculo.preco, custo, veiculo.preco, data_ent, veiculo.status, veiculo.loja_id)
    )
    conn.commit()
    vid = cursor.lastrowid
    cursor.execute("SELECT * FROM veiculo WHERE id = ?", (vid,))
    row = dict(cursor.fetchone())
    conn.close()
    return row

# ==================== Endpoints: Vendas e Manutenções ====================

@app.post("/vendas", status_code=status.HTTP_201_CREATED)
def registrar_venda(venda: VendaCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM veiculo WHERE id = ?", (venda.veiculo_id,))
    v = cursor.fetchone()
    if not v:
        conn.close()
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    if v["status"] != "disponivel":
        conn.close()
        raise HTTPException(status_code=400, detail="Veículo não está disponível para venda")
        
    custo_veiculo = v["custo_aquisicao"] if v["custo_aquisicao"] else 0.0
    lucro_base = venda.valor - custo_veiculo
    lucro_combinado = lucro_base

    # Se há trade-in associado, buscar dados de margem combinada
    if venda.tradein_id:
        cursor.execute("SELECT * FROM avaliacao_tradein WHERE id = ?", (venda.tradein_id,))
        t_row = cursor.fetchone()
        if t_row:
            lucro_combinado = t_row["margem_combinada_reais"]
            cursor.execute("UPDATE avaliacao_tradein SET status = 'concluido' WHERE id = ?", (venda.tradein_id,))

    cursor.execute(
        """
        INSERT INTO venda (veiculo_id, cliente_id, vendedor_id, tradein_id, pacote_manutencao_id, lucro_combinado, data, valor, tipo_pagamento) 
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?, ?)
        """,
        (venda.veiculo_id, venda.cliente_id, venda.vendedor_id, venda.tradein_id, venda.pacote_manutencao_id, lucro_combinado, venda.valor, venda.tipo_pagamento)
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

# ==================== Endpoints: Funcionários e Lojas ====================

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

# ==================== Endpoints: Autenticação ====================

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

# ==================== 1. MOTOR DE PRECIFICAÇÃO DINÂMICA & PÁTIO ====================

@app.get("/precificacao/patio/dashboard")
def dashboard_precificacao_patio():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM custo_patio_config ORDER BY id DESC LIMIT 1")
    config_row = cursor.fetchone()
    taxa_capital = config_row["taxa_custo_capital_anual"] if config_row else 0.12
    taxa_deprec = config_row["taxa_depreciacao_anual"] if config_row else 0.15
    taxa_seguro = config_row["taxa_seguro_anual"] if config_row else 0.012

    cursor.execute("SELECT * FROM veiculo WHERE status = 'disponivel' ORDER BY data_entrada ASC")
    veiculos = [dict(v) for v in cursor.fetchall()]
    conn.close()

    itens = []
    custo_total_carregamento_dia = 0.0
    custo_acumulado_total = 0.0
    veiculos_alerta_contagem = 0

    for v in veiculos:
        custo_aq = v.get("custo_aquisicao") or (v["preco"] * 0.85)
        dt_entrada = v.get("data_entrada") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        calc = calcular_custo_patio_veiculo(
            custo_aquisicao=float(custo_aq),
            preco_atual=float(v["preco"]),
            data_entrada_str=str(dt_entrada),
            taxa_capital_anual=taxa_capital,
            taxa_depreciacao_anual=taxa_deprec,
            taxa_seguro_anual=taxa_seguro
        )
        
        custo_total_carregamento_dia += calc["custo_diario"]
        custo_acumulado_total += calc["custo_patio_acumulado"]
        if calc["status_aging"] in ("ALERTA_AMARELO", "ALERTA_VERMELHO"):
            veiculos_alerta_contagem += 1

        itens.append({
            "veiculo_id": v["id"],
            "marca": v["marca"],
            "modelo": v["modelo"],
            "ano": v["ano"],
            "preco_atual": v["preco"],
            "custo_aquisicao": custo_aq,
            "data_entrada": dt_entrada,
            "dias_em_estoque": calc["dias_em_estoque"],
            "custo_diario": calc["custo_diario"],
            "custo_patio_acumulado": calc["custo_patio_acumulado"],
            "status_aging": calc["status_aging"],
            "desconto_sugerido": calc["desconto_sugerido"],
            "novo_preco_sugerido": calc["novo_preco_sugerido"],
            "piso_seguranca": calc["piso_seguranca"]
        })

    return {
        "total_veiculos_patio": len(veiculos),
        "custo_total_carregamento_dia": round(custo_total_carregamento_dia, 2),
        "custo_acumulado_patio_total": round(custo_acumulado_total, 2),
        "veiculos_alerta_contagem": veiculos_alerta_contagem,
        "itens": itens
    }

@app.post("/precificacao/veiculos/{veiculo_id}/aplicar-reajuste")
def aplicar_reajuste_preco(veiculo_id: int, req: ReajustePrecoRequest):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM veiculo WHERE id = ?", (veiculo_id,))
    v = cursor.fetchone()
    if not v:
        conn.close()
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    preco_anterior = v["preco"]
    cursor.execute("UPDATE veiculo SET preco = ? WHERE id = ?", (req.novo_preco, veiculo_id))
    conn.commit()
    conn.close()

    return {
        "veiculo_id": veiculo_id,
        "preco_anterior": preco_anterior,
        "preco_novo": req.novo_preco,
        "motivo": req.motivo,
        "mensagem": f"Preço atualizado com sucesso de R$ {preco_anterior:,.2f} para R$ {req.novo_preco:,.2f}"
    }

# ==================== 2. AVALIADOR DE TRADE-IN INTELIGENTE ====================

@app.post("/tradein/avaliar")
def avaliar_tradein(req: TradeInAvaliacaoRequest):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM veiculo WHERE id = ?", (req.veiculo_desejado_id,))
    v = cursor.fetchone()
    conn.close()

    if not v:
        raise HTTPException(status_code=404, detail="Veículo desejado não encontrado no estoque")

    custo_aq_novo = v["custo_aquisicao"] if v["custo_aquisicao"] else (v["preco"] * 0.85)
    
    resultado = calcular_tradein_margem_combinada(
        preco_venda_novo=float(v["preco"]),
        custo_aquisicao_novo=float(custo_aq_novo),
        preco_fipe_usado=req.preco_fipe,
        custo_recondicionamento_est=req.custo_recondicionamento_est,
        valor_proposto_usado=req.valor_proposto_usado,
        margem_alvo_revenda=req.margem_alvo_revenda or 0.15
    )

    resultado["veiculo_desejado"]["id"] = v["id"]
    resultado["veiculo_desejado"]["marca"] = v["marca"]
    resultado["veiculo_desejado"]["modelo"] = v["modelo"]
    resultado["veiculo_desejado"]["ano"] = v["ano"]

    return resultado

@app.post("/tradein/salvar", status_code=status.HTTP_201_CREATED)
def salvar_avaliacao_tradein(req: TradeInSalvarRequest):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO avaliacao_tradein (
            cliente_id, veiculo_desejado_id, vendedor_id, marca_usado, modelo_usado, ano_usado,
            km_usado, preco_fipe, custo_recondicionamento_est, oferta_ideal_sugerida,
            valor_proposto_usado, overallowance, lucro_veiculo_novo, margem_futura_usado,
            margem_combinada_reais, margem_combinada_percentual, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            req.cliente_id, req.veiculo_desejado_id, req.vendedor_id, req.marca_usado, req.modelo_usado,
            req.ano_usado, req.km_usado, req.preco_fipe, req.custo_recondicionamento_est,
            req.oferta_ideal_sugerida, req.valor_proposto_usado, req.overallowance,
            req.lucro_veiculo_novo, req.margem_futura_usado, req.margem_combinada_reais,
            req.margem_combinada_percentual, req.status
        )
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    return {
        "id": novo_id,
        "status": req.status,
        "mensagem": "Avaliação de Trade-In registrada e apta para inclusão na venda"
    }

@app.get("/tradein/historico")
def listar_historico_tradein():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.*, v.modelo as modelo_desejado, v.marca as marca_desejada
        FROM avaliacao_tradein t
        LEFT JOIN veiculo v ON t.veiculo_desejado_id = v.id
        ORDER BY t.id DESC
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

# ==================== 3. SIMULADOR DE COMBOS FINANCIAMENTO + MANUTENÇÃO ====================

@app.get("/combos/pacotes")
def listar_pacotes_manutencao():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacote_manutencao WHERE ativo = 1 ORDER BY preco_tabela ASC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

@app.post("/combos/simular-financiamento")
def simular_financiamento_combo(req: SimuladorComboRequest):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM veiculo WHERE id = ?", (req.veiculo_id,))
    v = cursor.fetchone()
    if not v:
        conn.close()
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    preco_pacote = 0.0
    nome_pacote = "Sem Pacote Adicional"

    if req.pacote_manutencao_id:
        cursor.execute("SELECT * FROM pacote_manutencao WHERE id = ?", (req.pacote_manutencao_id,))
        p = cursor.fetchone()
        if p:
            preco_pacote = p["preco_tabela"]
            nome_pacote = p["nome"]
    else:
        cursor.execute("SELECT * FROM pacote_manutencao WHERE ativo = 1 ORDER BY id ASC LIMIT 1")
        p = cursor.fetchone()
        if p:
            preco_pacote = p["preco_tabela"]
            nome_pacote = p["nome"]

    conn.close()

    res = simular_combo_financiamento(
        preco_veiculo=float(v["preco"]),
        valor_entrada=req.valor_entrada,
        num_parcelas=req.num_parcelas,
        taxa_juros_mensal=req.taxa_juros_mensal,
        preco_pacote_manutencao=preco_pacote,
        nome_pacote=nome_pacote
    )

    res["veiculo_info"] = {
        "id": v["id"],
        "marca": v["marca"],
        "modelo": v["modelo"],
        "ano": v["ano"]
    }

    return res
