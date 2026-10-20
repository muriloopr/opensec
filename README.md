# 🚗 Sistema de Gestão de Concessionária

Aplicação web completa para gestão de redes de concessionárias de veículos, centralizando o controle de estoque, equipes, vendas, financiamentos e manutenções em um único lugar.

---

## 🎯 1. Problema que Resolvemos
Gerenciar uma concessionária (ou rede de lojas) envolve lidar com múltiplos processos descentralizados: controle de estoque de veículos, comissões de vendedores, ordens de serviço de mecânicos, cadastros de clientes e acompanhamento de financiamentos bancários. 

O sistema elimina planilhas desorganizadas e processos manuais propensos a erros, centralizando todas as operações em uma interface intuitiva e conectada em tempo real com backend em nuvem (Xano).

---

## 👥 2. Público-Alvo
* **Gerentes de Concessionária:** Necessitam de uma visão rápida e consolidada dos indicadores da rede (Dashboard Executivo, faturamento e veículos vendidos/disponíveis).
* **Vendedores:** Precisam consultar rapidamente o estoque de veículos disponíveis por preço/marca e registrar novas vendas ou financiamentos com agilidade.
* **Mecânicos / Equipe de Pós-Venda:** Precisam abrir e acompanhar ordens de manutenção e revisão de veículos.
* **Administradores:** Precisam gerenciar o cadastro de lojas, funcionários e permissões de acesso.

---

## 🚀 3. Escopo do MVP (Minimum Viable Product)

O MVP entrega um sistema funcional de ponta a ponta dividido nas seguintes funcionalidades principais:

1. **Dashboard Executivo:**
   * Indicadores de desempenho (KPIs) com total de veículos no escopo, disponíveis, vendidos, em manutenção e valor total investido no estoque.
   * Gráficos interativos de distribuição de veículos por status e por marca.
2. **Barra Lateral Avançada:**
   * Indicador de status de conexão com a API em tempo real.
   * Filtro global de loja para segmentar toda a operação.
3. **Gestão de Estoque de Veículos:**
   * Listagem completa com filtros avançados por status (`disponivel`, `vendido`, `em_manutencao`), busca textual por marca/modelo e slider de preço máximo.
   * Formulário para cadastro de novos veículos.
4. **Registro de Vendas e Financiamentos:**
   * Seleção de veículos disponíveis no estoque para efetuar vendas à vista ou financiadas associando clientes e vendedores.
5. **Histórico de Veículos Vendidos:**
   * Aba dedicada para acompanhamento dos veículos que já foram comercializados pela rede.
6. **Ordens de Manutenção:**
   * Abertura de chamados de revisão e manutenção para mecânicos, atualizando automaticamente o status do veículo.
7. **Gestão de Lojas e Funcionários:**
   * Visualização das unidades da rede (lojas) e de suas equipes (gerentes, vendedores e mecânicos).

---

## 🛠️ 4. Arquitetura e Tecnologias
* **Frontend:** Streamlit (Python) - Interface web reativa e moderna.
* **Backend:** FastAPI (Python) - API REST robusta com validação Pydantic.
* **Banco de Dados / Regras de Negócio:** Xano (XanoScript / Cloud BaaS).
* **Testes Automatizados:** Pytest (na pasta `tests/`).

---

## ⚙️ 5. Como Instalar e Rodar

### Pré-requisitos
* Python 3.12 ou superior instalado.
* Gerenciador de pacotes `uv` ou `pip`.

### Passos para execução:

1. **Criar e ativar o ambiente virtual (Python 3.12):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Instalar as dependências:**
   ```powershell
   uv pip install -r backend/requirements.txt
   uv pip install -r frontend/requirements.txt
   ```

3. **Rodar os Testes Automatizados:**
   ```powershell
   python -m pytest
   ```

4. **Rodar o Backend (FastAPI):**
   ```powershell
   uvicorn backend.main:app --reload --port 8000
   ```
   *(Acesse a documentação Swagger em `http://127.0.0.1:8000/docs`)*

5. **Rodar o Frontend (Streamlit) em outro terminal:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   streamlit run frontend/app.py
   ```
   *(Acesse a interface web em `http://localhost:8501`)*
