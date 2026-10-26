# Tarefas: Motor de Precificação Dinâmica & Trade-In com Inteligência de Margem

## 1. Migração de Banco de Dados e Modelagem (SQLite / Xano)

- [x] 1.1 Atualizar `backend/main.py` para incluir novas colunas nas tabelas existentes:
  * Em `veiculo`: adicionar `custo_aquisicao` (REAL), `data_entrada` (TEXT), `preco_original` (REAL).
  * Em `venda`: adicionar `tradein_id` (INTEGER NULL), `pacote_manutencao_id` (INTEGER NULL), `lucro_combinado` (REAL).
- [x] 1.2 Criar tabelas novas no SQLite (`init_db()` em `backend/main.py`):
  * `custo_patio_config` (taxa_custo_capital_anual, taxa_depreciacao_anual, taxa_seguro_anual, dias_gatilho_alerta).
  * `avaliacao_tradein` (registro detalhado do seminovo, fipe, custos de recondicionamento e margens calculadas).
  * `pacote_manutencao` (catalogo de revisões e combos).
- [x] 1.3 Popular dados de semente (seed) no `init_db()`:
  * Inserir configuração padrão de taxas em `custo_patio_config`.
  * Inserir 2 pacotes padrão de revisão em `pacote_manutencao` (Plano Bronze 1 ano e Plano Prata 2 anos).
  * Atualizar os registros de teste da tabela `veiculo` com datas de entrada retroativas (para testar os alertas de >30 dias).

---

## 2. Implementação dos Serviços de Domínio e Lógicas de Negócio (`backend/services/`)

- [x] 2.1 Criar `backend/services/pricing_engine.py`:
  * Implementar cálculo de custo diário de carregar veículo (`taxa_capital + taxa_depreciacao + taxa_seguro`).
  * Implementar algoritmo de aging e sugestão de desconto escalonado (faixa 31-45 dias vs. >45 dias) com piso de proteção de margem.
- [x] 2.2 Criar `backend/services/tradein_engine.py`:
  * Implementar algoritmo de cálculo de oferta ótima de trade-in a partir de valor FIPE e custo de recondicionamento.
  * Implementar cálculo de overallowance e projeção de margem futura do usado.
  * Implementar consolidação da **Margem Combinada da Operação** (Lucro do Estoque - Desconto + Margem Futura) e verificação do piso de segurança (8%).
- [x] 2.3 Criar `backend/services/combo_engine.py`:
  * Implementar amortização pela Tabela Price para parcelas convencionais e parcelas com pacote agregado.
  * Calcular delta de prestação mensal, economia estimada de balcão e projeção de comissão financeira.

---

## 3. Schemas Pydantic e Endpoints REST (`backend/main.py`)

- [x] 3.1 Definir schemas Pydantic para requests e responses:
  * `ReajustePrecoRequest`, `DashboardPatioResponse`.
  * `TradeInAvaliacaoRequest`, `TradeInAvaliacaoResponse`, `TradeInSalvarRequest`.
  * `SimuladorComboRequest`, `SimuladorComboResponse`.
- [x] 3.2 Implementar endpoints de Precificação Dinâmica:
  * `GET /precificacao/patio/dashboard`
  * `POST /precificacao/veiculos/{id}/aplicar-reajuste`
- [x] 3.3 Implementar endpoints de Avaliação de Trade-In:
  * `POST /tradein/avaliar`
  * `POST /tradein/salvar`
  * `GET /tradein/historico`
- [x] 3.4 Implementar endpoints do Simulador de Financiamento & Combos:
  * `GET /combos/pacotes`
  * `POST /combos/simular-financiamento`
- [x] 3.5 Ajustar endpoint existente `POST /vendas` para suportar `tradein_id`, `pacote_manutencao_id` e computar `lucro_combinado`.

---

## 4. Interface do Usuário (`frontend/app.py` - Streamlit)

- [x] 4.1 Adicionar novas abas de navegação no menu lateral do Streamlit:
  * "📊 Precificação & Custo de Pátio"
  * "🔄 Avaliador de Trade-In"
  * "💳 Financiamento & Combos"
- [x] 4.2 Construir tela "Precificação & Custo de Pátio":
  * Cards de topo com `st.metric` (Total em Pátio, Custo Diário Consolidado, Carros em Alerta > 30 dias).
  * Tabela com badges visuais de criticidade (`ALERTA_AMARELO`, `ALERTA_VERMELHO`).
  * Botão de ação rápida "Aplicar Desconto Sugerido" disparando chamada POST para a API.
- [x] 4.3 Construir tela "Avaliador de Trade-In":
  * Formulário interativo de entrada de dados do veículo usado (marca, modelo, ano, km, FIPE informada, custo de funilaria/revisão).
  * Painel de resultado em tempo real exibindo a Margem Combinada (em R$ e %) com alerta visual verde/vermelho caso atinja ou fira o piso de 8%.
  * Botão "Vincular Trade-In à Venda".
- [x] 4.4 Construir tela "Financiamento & Combos":
  * Sliders para valor de entrada, prazo (meses) e seleção do combo de manutenção.
  * Comparativo lado a lado em cards estilizados mostrando a parcela comum vs. combo, e destaque "Por apenas +R$ X/mês".

---

## 5. Testes Automatizados e Homologação (`backend/test_pricing_tradein.py`)

- [x] 5.1 Criar testes unitários para as fórmulas matemáticas em `pricing_engine`, `tradein_engine` e `combo_engine`.
- [x] 5.2 Criar testes de integração da API FastAPI para os endpoints de aging, trade-in e combos.
- [x] 5.3 Validar cobertura de casos de borda: veículo vendido com 0 dias de pátio, trade-in com valor muito acima da FIPE (rejeição automática por margem combinada < 8%), e simulação com entrada de 0%.

---

## Trechos de Código Essenciais para Implementação

### Trecho 1: Lógica do Motor de Precificação e Aging (`backend/services/pricing_engine.py`)
```python
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
    # Converter data e calcular dias em estoque
    data_entrada = datetime.fromisoformat(data_entrada_str.replace("Z", ""))
    dias_em_estoque = max(0, (datetime.now() - data_entrada).days)
    
    # Custo diário composto
    taxa_diaria = (taxa_capital_anual + taxa_depreciacao_anual + taxa_seguro_anual) / 365.0
    custo_diario = round(custo_aquisicao * taxa_diaria, 2)
    custo_patio_acumulado = round(custo_diario * dias_em_estoque, 2)
    
    # Avaliação de aging e recomendação de reajuste
    if dias_em_estoque <= 30:
        status_aging = "NORMAL"
        desconto_sugerido = 0.0
    elif dias_em_estoque <= 45:
        status_aging = "ALERTA_AMARELO"
        # Desconto de giro suave: até 4% do preço ou o custo acumulado
        desconto_sugerido = round(min(preco_atual * 0.04, custo_patio_acumulado), 2)
    else:
        status_aging = "ALERTA_VERMELHO"
        # Desconto agressivo para desovar: até 7% do preço ou 1.25x o custo de pátio
        desconto_sugerido = round(min(preco_atual * 0.07, custo_patio_acumulado * 1.25), 2)
        
    novo_preco_sugerido = round(preco_atual - desconto_sugerido, 2)
    piso_seguranca = round(custo_aquisicao * 1.02, 2)
    
    if novo_preco_sugerido < piso_seguranca:
        novo_preco_sugerido = piso_seguranca
        desconto_sugerido = round(preco_atual - novo_preco_sugerido, 2)
        
    return {
        "dias_em_estoque": dias_em_estoque,
        "custo_diario": custo_diario,
        "custo_patio_acumulado": custo_patio_acumulado,
        "status_aging": status_aging,
        "desconto_sugerido": desconto_sugerido,
        "novo_preco_sugerido": novo_preco_sugerido
    }
```

---

### Trecho 2: Lógica do Avaliador de Trade-In e Margem Combinada (`backend/services/tradein_engine.py`)
```python
from typing import Dict, Any

def calcular_tradein_margem_combinada(
    preco_venda_novo: float,
    custo_aquisicao_novo: float,
    preco_fipe_usado: float,
    custo_recondicionamento_est: float,
    valor_proposto_usado: float,
    margem_alvo_revenda: float = 0.15
) -> Dict[str, Any]:
    # 1. Perna do Carro em Estoque (Novo ou Seminovo vendido)
    lucro_bruto_novo = preco_venda_novo - custo_aquisicao_novo
    
    # 2. Perna do Carro Usado de Entrada (Trade-In)
    # Oferta ideal considera a FIPE com margem de segurança de revenda menos recondicionamento
    oferta_ideal_sugerida = round(preco_fipe_usado * (1.0 - margem_alvo_revenda) - custo_recondicionamento_est, 2)
    
    # Overallowance: se a concessionária pagou mais no usado do que a oferta ideal
    overallowance = round(max(0.0, valor_proposto_usado - oferta_ideal_sugerida), 2)
    
    # Margem projetada na futura revenda do carro recebido
    custo_total_usado = valor_proposto_usado + custo_recondicionamento_est
    margem_futura_usado = round(preco_fipe_usado - custo_total_usado, 2)
    
    # 3. Consolidação da Margem Combinada
    margem_combinada_reais = round(lucro_bruto_novo - overallowance + max(0.0, margem_futura_usado), 2)
    base_transacao = preco_venda_novo + preco_fipe_usado
    margem_combinada_pct = round((margem_combinada_reais / base_transacao) * 100, 2) if base_transacao > 0 else 0.0
    
    status_aprovacao = "APROVADO" if margem_combinada_pct >= 8.0 else "REQUER_ALCADA_GERENCIAL"
    
    return {
        "lucro_bruto_novo": lucro_bruto_novo,
        "oferta_ideal_sugerida": oferta_ideal_sugerida,
        "overallowance": overallowance,
        "margem_futura_usado": margem_futura_usado,
        "margem_combinada_reais": margem_combinada_reais,
        "margem_combinada_percentual": margem_combinada_pct,
        "status_aprovacao": status_aprovacao,
        "requer_alcada": status_aprovacao == "REQUER_ALCADA_GERENCIAL"
    }
```

---

### Trecho 3: Simulador de Financiamento Price e Combos (`backend/services/combo_engine.py`)
```python
from typing import Dict, Any

def calcular_parcela_price(saldo_devedor: float, taxa_mensal: float, meses: int) -> float:
    if taxa_mensal == 0:
        return round(saldo_devedor / meses, 2)
    fator = (1 + taxa_mensal) ** meses
    pmt = saldo_devedor * (taxa_mensal * fator) / (fator - 1)
    return round(pmt, 2)

def simular_combo_financiamento(
    preco_veiculo: float,
    valor_entrada: float,
    num_parcelas: int,
    taxa_juros_mensal: float,
    preco_pacote_manutencao: float,
    nome_pacote: str
) -> Dict[str, Any]:
    # Financiamento Tradicional
    saldo_tradicional = max(0.0, preco_veiculo - valor_entrada)
    pmt_tradicional = calcular_parcela_price(saldo_tradicional, taxa_juros_mensal, num_parcelas)
    total_pago_tradicional = round(pmt_tradicional * num_parcelas, 2)
    
    # Financiamento com Combo Embutido
    saldo_combo = saldo_tradicional + preco_pacote_manutencao
    pmt_combo = calcular_parcela_price(saldo_combo, taxa_juros_mensal, num_parcelas)
    total_pago_combo = round(pmt_combo * num_parcelas, 2)
    
    diferenca_mensal = round(pmt_combo - pmt_tradicional, 2)
    economia_cliente = round(preco_pacote_manutencao * 0.30, 2) # Estimativa de 30% vs balcão avulso
    comissao_loja_extra = round(preco_pacote_manutencao * 0.015, 2) # Retorno de F&I
    
    return {
        "tradicional": {
            "saldo_financiado": saldo_tradicional,
            "parcela_mensal": pmt_tradicional,
            "total_pago": total_pago_tradicional
        },
        "combo": {
            "pacote_nome": nome_pacote,
            "pacote_valor": preco_pacote_manutencao,
            "saldo_financiado": saldo_combo,
            "parcela_mensal": pmt_combo,
            "total_pago": total_pago_combo,
            "diferenca_mensal": diferenca_mensal,
            "economia_cliente": economia_cliente,
            "comissao_loja_extra": comissao_loja_extra
        }
    }
```
