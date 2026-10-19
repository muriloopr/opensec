design técnico: dashboard e melhorias de ux
1. arquitetura e componentes
frontend (streamlit):

usa st.session_state pra guardar o loja_selecionada_id (com a opção "todas").

o seletor na st.sidebar puxa da api /lojas (ou monta direto com base nos veículos), junto do indicador de status da api.

aba dashboard usa st.metric pros kpis e st.bar_chart / st.altair_chart pra exibir a distribuição dos dados.

backend (fastapi):

reutiliza os endpoints que já existem (/veiculos, etc.). as agregações podem ser feitas direto no streamlit pra ir mais rápido.

2. fluxo de dados
assim que autentica, o streamlit carrega as lojas e veículos.

o usuário seleciona a loja na barra lateral.

as abas (dashboard, estoque, vendas e manutenção) aplicam esse filtro globalmente.