import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Sistema de Concessionária", page_icon="🚗", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = ""
    st.session_state["access_token"] = ""

st.title("🚗 Sistema de Gestão de Concessionária")

if not st.session_state["authenticated"]:
    st.subheader("🔐 Área de Autenticação")
    tab_login, tab_signup = st.tabs(["Login", "Registar Conta"])
    
    with tab_login:
        with st.form("form_login"):
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            submit_login = st.form_submit_button("Entrar")
            if submit_login:
                try:
                    r = requests.post(f"{API_URL}/auth/login", json={"email": email, "senha": senha})
                    if r.status_code == 200:
                        data = r.json()
                        st.session_state["authenticated"] = True
                        st.session_state["user_email"] = data["email"]
                        st.session_state["access_token"] = data["access_token"]
                        st.success("Login efetuado com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro: {r.json().get('detail', r.text)}")
                except Exception as e:
                    st.error(f"Erro de conexão com o backend: {e}")
                    
    with tab_signup:
        with st.form("form_signup"):
            email_s = st.text_input("Email para Registo")
            senha_s = st.text_input("Senha", type="password")
            submit_signup = st.form_submit_button("Criar Conta")
            if submit_signup:
                try:
                    r = requests.post(f"{API_URL}/auth/signup", json={"email": email_s, "senha": senha_s})
                    if r.status_code == 201:
                        st.success("Conta criada com sucesso! Pode efetuar login na aba ao lado.")
                    else:
                        st.error(f"Erro: {r.json().get('detail', r.text)}")
                except Exception as e:
                    st.error(f"Erro de conexão com o backend: {e}")
else:
    st.sidebar.success(f"Logado como: {st.session_state['user_email']}")
    if st.sidebar.button("Terminar Sessão"):
        st.session_state["authenticated"] = False
        st.session_state["user_email"] = ""
        st.session_state["access_token"] = ""
        st.rerun()

    st.sidebar.title("Navegação")
    menu = st.sidebar.selectbox("Escolha uma opção", ["Estoque de Veículos", "Registrar Venda", "Ordens de Manutenção", "Funcionários e Lojas"])

    if menu == "Estoque de Veículos":
        st.header("📦 Estoque de Veículos")
        
        status_filter = st.selectbox("Filtrar por Status", ["Todos", "disponivel", "vendido", "em_manutencao"])
        
        try:
            url = f"{API_URL}/veiculos"
            if status_filter != "Todos":
                url += f"?status={status_filter}"
            res = requests.get(url)
            veiculos = res.json()
            
            if veiculos:
                st.dataframe(veiculos, use_container_width=True)
            else:
                st.info("Nenhum veículo encontrado.")
        except Exception as e:
            st.error(f"Erro ao conectar com o backend FastAPI: {e}")
            
        st.divider()
        st.subheader("Adicionar Novo Veículo")
        with st.form("form_veiculo"):
            marca = st.text_input("Marca")
            modelo = st.text_input("Modelo")
            ano = st.number_input("Ano", min_value=1950, max_value=2030, value=2024)
            preco = st.number_input("Preço (R$)", min_value=0.0, value=50000.0)
            status_v = st.selectbox("Status Inicial", ["disponivel", "vendido", "em_manutencao"])
            loja_id = st.number_input("ID da Loja", min_value=1, value=1)
            
            submit = st.form_submit_button("Cadastrar Veículo")
            if submit:
                payload = {
                    "marca": marca,
                    "modelo": modelo,
                    "ano": int(ano),
                    "preco": float(preco),
                    "status": status_v,
                    "loja_id": int(loja_id)
                }
                try:
                    r = requests.post(f"{API_URL}/veiculos", json=payload)
                    if r.status_code == 201:
                        st.success("Veículo cadastrado com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro: {r.text}")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")

    elif menu == "Registrar Venda":
        st.header("💰 Registrar Venda de Veículo")
        
        with st.form("form_venda"):
            veiculo_id = st.number_input("ID do Veículo", min_value=1, value=1)
            cliente_id = st.number_input("ID do Cliente", min_value=1, value=1)
            vendedor_id = st.number_input("ID do Vendedor (Funcionário)", min_value=1, value=2)
            valor = st.number_input("Valor da Venda (R$)", min_value=0.0, value=50000.0)
            tipo_pagamento = st.selectbox("Tipo de Pagamento", ["venda", "financiamento"])
            
            submit_venda = st.form_submit_button("Efetuar Venda")
            if submit_venda:
                payload = {
                    "veiculo_id": int(veiculo_id),
                    "cliente_id": int(cliente_id),
                    "vendedor_id": int(vendedor_id),
                    "valor": float(valor),
                    "tipo_pagamento": tipo_pagamento
                }
                try:
                    r = requests.post(f"{API_URL}/vendas", json=payload)
                    if r.status_code == 201:
                        st.success("Venda registrada com sucesso! Veículo marcado como vendido.")
                    else:
                        st.error(f"Erro: {r.json().get('detail', r.text)}")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")

    elif menu == "Ordens de Manutenção":
        st.header("🔧 Registrar Manutenção")
        
        with st.form("form_manutencao"):
            veiculo_id = st.number_input("ID do Veículo", min_value=1, value=1)
            mecanico_id = st.number_input("ID do Mecânico (Funcionário)", min_value=1, value=3)
            descricao = st.text_area("Descrição do Serviço")
            custo = st.number_input("Custo (R$)", min_value=0.0, value=500.0)
            
            submit_m = st.form_submit_button("Registrar Manutenção")
            if submit_m:
                payload = {
                    "veiculo_id": int(veiculo_id),
                    "mecanico_id": int(mecanico_id),
                    "descricao": descricao,
                    "custo": float(custo)
                }
                try:
                    r = requests.post(f"{API_URL}/manutencoes", json=payload)
                    if r.status_code == 201:
                        st.success("Manutenção registrada! Veículo em manutenção.")
                    else:
                        st.error(f"Erro: {r.text}")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")

    elif menu == "Funcionários e Lojas":
        st.header("🏢 Lojas e Funcionários")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Lojas Cadastradas")
            try:
                r = requests.get(f"{API_URL}/lojas")
                lojas = r.json()
                if lojas:
                    st.dataframe(lojas, use_container_width=True)
                else:
                    st.info("Nenhuma loja cadastrada.")
            except Exception as e:
                st.error(f"Erro: {e}")
                
        with col2:
            st.subheader("Funcionários")
            try:
                r = requests.get(f"{API_URL}/funcionarios")
                funcs = r.json()
                if funcs:
                    st.dataframe(funcs, use_container_width=True)
                else:
                    st.info("Nenhum funcionário cadastrado.")
            except Exception as e:
                st.error(f"Erro: {e}")
