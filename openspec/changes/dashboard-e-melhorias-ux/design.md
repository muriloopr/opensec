# Design Técnico: Dashboard e Melhorias UX

## 1. Arquitetura e Componentes
- **Frontend (Streamlit)**:
  - Utilizará `st.session_state` para armazenar `loja_selecionada_id` (com opção "Todas").
  - `st.sidebar` receberá o seletor de lojas carregado da API `/lojas` (ou listadas a partir de veículos) e indicador de status da API.
  - Nova aba `📊 Dashboard` utilizando `st.metric` para KPIs e `st.bar_chart` / `st.altair_chart` para distribuições.
- **Backend (FastAPI)**:
  - Aproveitar endpoints existentes (`/veiculos`, etc.) ou consumir dados diretamente. Se necessário, agregar no cliente Streamlit para manter agilidade.

## 2. Fluxo de Dados
1. Ao iniciar a sessão autenticada, o Streamlit busca lojas e veículos.
2. Na barra lateral, o usuário escolhe a loja.
3. Todas as abas (Dashboard, Estoque, Vendas, Manutenção) respeitam o filtro da loja selecionada no estado global.
