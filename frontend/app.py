import os
import streamlit as st
import requests

# Bypass do proxy local do Windows para requisições ao FastAPI
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Sistema de Concessionária",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = ""
    st.session_state["access_token"] = ""
    st.session_state["filtro_loja_id"] = "Todas"

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
                    r = requests.post(f"{API_URL}/auth/login", json={"email": email, "senha": senha}, timeout=35)
                    if r.status_code == 200:
                        data = r.json()
                        st.session_state["authenticated"] = True
                        st.session_state["user_email"] = data["email"]
                        st.session_state["access_token"] = data["access_token"]
                        st.toast("Login efetuado com sucesso!", icon="✅")
                        st.rerun()
                    else:
                        st.error(f"Erro: {r.json().get('detail', r.text)}")
                except Exception as e:
                    st.error(f"Erro de conexão com o backend: {e}")
                    
    with tab_signup:
        with st.form("form_signup"):
            email_s = st.text_input("Email para Registo")
            senha_s = st.text_input("Senha", type="password", help="A senha deve ter pelo menos 8 caracteres")
            submit_signup = st.form_submit_button("Criar Conta")
            if submit_signup:
                if len(senha_s) < 8:
                    st.warning("⚠️ A senha deve ter no mínimo 8 caracteres.")
                elif not email_s or "@" not in email_s:
                    st.warning("⚠️ Informe um e-mail válido.")
                else:
                    try:
                        r = requests.post(f"{API_URL}/auth/signup", json={"email": email_s, "senha": senha_s}, timeout=35)
                        if r.status_code == 201:
                            st.success("Conta criada com sucesso! Pode efetuar login na aba ao lado.")
                        else:
                            st.error(f"Erro: {r.json().get('detail', r.text)}")
                    except Exception as e:
                        st.error(f"Erro de conexão com o backend: {e}")
else:
    # --- BARRA LATERAL AVANÇADA ---
    st.sidebar.markdown(f"### 👤 Utilizador\n**{st.session_state['user_email']}**")
    
    # Status de Conexão com API
    try:
        r_ping = requests.get(f"{API_URL}/veiculos", timeout=3)
        if r_ping.status_code == 200:
            st.sidebar.success("🟢 API Conectada (Xano Cloud)")
        else:
            st.sidebar.warning("🟡 API Online com Alerta")
    except Exception:
        st.sidebar.error("🔴 API Offline / Indisponível")

    st.sidebar.divider()
    
    # Seletor Global de Loja
    st.sidebar.markdown("### 🏢 Filtro Global")
    lojas_disponiveis = ["Todas"]
    try:
        r_l = requests.get(f"{API_URL}/lojas", timeout=5)
        if r_l.status_code == 200:
            for l_obj in r_l.json():
                lojas_disponiveis.append(f"Loja #{l_obj.get('id')} - {l_obj.get('nome', 'Matriz')}")
    except Exception:
        pass

    loja_selecionada = st.sidebar.selectbox("Filtrar por Loja", lojas_disponiveis)
    st.session_state["filtro_loja_id"] = loja_selecionada

    st.sidebar.divider()
    if st.sidebar.button("🚪 Terminar Sessão", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["user_email"] = ""
        st.session_state["access_token"] = ""
        st.rerun()

    # Navegação por Abas Principais (Com Dashboard e Vendas)
    tab_dash, tab_estoque, tab_venda, tab_historico_vendas, tab_manut, tab_equipe = st.tabs([
        "📊 Dashboard Executivo",
        "📦 Estoque de Veículos",
        "💰 Registrar Venda",
        "📋 Histórico de Vendas",
        "🔧 Ordens de Manutenção",
        "🏢 Funcionários e Lojas"
    ])

    # Obter todos os veículos base
    veiculos_todos = []
    try:
        res_all = requests.get(f"{API_URL}/veiculos", timeout=30)
        if res_all.status_code == 200:
            veiculos_todos = res_all.json()
    except Exception:
        pass

    # Aplicar filtro global de loja se selecionada
    if loja_selecionada != "Todas":
        # Extrair o ID da loja da string ex: "Loja #1 - Matriz" -> id 1
        try:
            loja_id_filtro = int(loja_selecionada.split("#")[1].split(" ")[0])
            veiculos_todos = [v for v in veiculos_todos if v.get("loja_id") == loja_id_filtro]
        except Exception:
            pass

    # --- ABA 0: DASHBOARD EXECUTIVO ---
    with tab_dash:
        st.subheader("📊 Dashboard Executivo da Rede")
        
        total = len(veiculos_todos)
        disp = sum(1 for v in veiculos_todos if v.get("status") == "disponivel")
        vend = sum(1 for v in veiculos_todos if v.get("status") == "vendido")
        manu = sum(1 for v in veiculos_todos if v.get("status") == "em_manutencao")
        valor_total_estoque = sum(float(v.get("preco", 0)) for v in veiculos_todos if v.get("status") == "disponivel")

        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        col_m1.metric("Veículos no Escopo", total)
        col_m2.metric("Disponíveis", disp)
        col_m3.metric("Vendidos", vend)
        col_m4.metric("Em Manutenção", manu)
        col_m5.metric("Valor em Estoque", f"R$ {valor_total_estoque:,.2f}")

        st.divider()

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("#### 🚗 Distribuição por Status")
            status_counts = {"Disponível": disp, "Vendido": vend, "Manutenção": manu}
            st.bar_chart(status_counts)

        with col_g2:
            st.markdown("#### 🏷️ Veículos por Marca")
            marcas_dict = {}
            for v in veiculos_todos:
                marca = v.get("marca", "Outros")
                marcas_dict[marca] = marcas_dict.get(marca, 0) + 1
            if marcas_dict:
                st.bar_chart(marcas_dict)
            else:
                st.info("Sem dados de marcas disponíveis.")

    # --- ABA 1: ESTOQUE DE VEÍCULOS ---
    with tab_estoque:
        st.subheader("Estoque de Veículos")

        # Filtros avançados na aba de estoque
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            status_filter = st.selectbox("Status", ["Todos", "disponivel", "vendido", "em_manutencao"])
        with col_f2:
            busca_texto = st.text_input("🔍 Buscar Marca ou Modelo", placeholder="Ex: Corolla, Toyota...")
        with col_f3:
            max_preco_val = max([float(v.get("preco", 100000)) for v in veiculos_todos], default=200000.0)
            filtro_preco = st.slider("Preço Máximo (R$)", min_value=0.0, max_value=max(max_preco_val, 200000.0), value=max(max_preco_val, 200000.0), step=5000.0)

        veiculos_exibidos = veiculos_todos
        if status_filter != "Todos":
            veiculos_exibidos = [v for v in veiculos_exibidos if v.get("status") == status_filter]
        
        if busca_texto:
            bt = busca_texto.lower()
            veiculos_exibidos = [v for v in veiculos_exibidos if bt in v.get("marca", "").lower() or bt in v.get("modelo", "").lower()]

        veiculos_exibidos = [v for v in veiculos_exibidos if float(v.get("preco", 0)) <= filtro_preco]

        if veiculos_exibidos:
            st.dataframe(veiculos_exibidos, use_container_width=True)
        else:
            st.info("Nenhum veículo encontrado para os filtros selecionados.")
            
        with st.expander("➕ Cadastrar Novo Veículo", expanded=False):
            with st.form("form_veiculo"):
                f_col1, f_col2 = st.columns(2)
                with f_col1:
                    marca = st.text_input("Marca")
                    modelo = st.text_input("Modelo")
                    ano = st.number_input("Ano", min_value=1950, max_value=2030, value=2024)
                with f_col2:
                    preco = st.number_input("Preço (R$)", min_value=0.0, value=75000.0, step=1000.0)
                    status_v = st.selectbox("Status Inicial", ["disponivel", "vendido", "em_manutencao"])
                    loja_id = st.number_input("ID da Loja", min_value=1, value=1)
                
                submit = st.form_submit_button("Salvar Veículo")
                if submit:
                    if not marca or not modelo:
                        st.warning("Preencha marca e modelo.")
                    else:
                        payload = {
                            "marca": marca,
                            "modelo": modelo,
                            "ano": int(ano),
                            "preco": float(preco),
                            "status": status_v,
                            "loja_id": int(loja_id)
                        }
                        try:
                            r = requests.post(f"{API_URL}/veiculos", json=payload, timeout=30)
                            if r.status_code == 201:
                                novo_id = r.json().get("id")
                                st.toast(f"Veículo #{novo_id} cadastrado com sucesso!", icon="🎉")
                                st.success(f"Veículo {marca} {modelo} cadastrado com ID #{novo_id}!")
                                st.rerun()
                            else:
                                st.error(f"Erro: {r.text}")
                        except Exception as e:
                            st.error(f"Erro de conexão: {e}")

    # --- ABA 2: REGISTRAR VENDA ---
    with tab_venda:
        st.subheader("Registrar Venda de Veículo")
        
        veiculos_disp = [v for v in veiculos_todos if v.get("status") == "disponivel"]
        
        if not veiculos_disp:
            st.info("Nenhum veículo disponível para venda no momento (verifique o filtro de loja).")
        else:
            opcoes_v = {f"#{v['id']} - {v['marca']} {v['modelo']} (R$ {v['preco']:,.2f})": v for v in veiculos_disp}
            veiculo_selecionado = st.selectbox("Selecione o Veículo Disponível", list(opcoes_v.keys()))
            obj_veiculo = opcoes_v[veiculo_selecionado]

            with st.form("form_venda"):
                v_col1, v_col2 = st.columns(2)
                with v_col1:
                    cliente_id = st.number_input("ID do Cliente", min_value=1, value=1)
                    vendedor_id = st.number_input("ID do Vendedor", min_value=1, value=2)
                with v_col2:
                    valor_venda = st.number_input("Valor da Venda (R$)", min_value=0.0, value=float(obj_veiculo.get("preco", 50000.0)), step=1000.0)
                    tipo_pagamento = st.selectbox("Tipo de Pagamento", ["venda", "financiamento"])
                
                submit_venda = st.form_submit_button("Efetuar Venda")
                if submit_venda:
                    payload = {
                        "veiculo_id": int(obj_veiculo["id"]),
                        "cliente_id": int(cliente_id),
                        "vendedor_id": int(vendedor_id),
                        "valor": float(valor_venda),
                        "tipo_pagamento": tipo_pagamento
                    }
                    try:
                        r = requests.post(f"{API_URL}/vendas", json=payload, timeout=30)
                        if r.status_code == 201:
                            venda_res = r.json()
                            st.toast(f"Venda #{venda_res.get('id')} concluída com sucesso!", icon="💰")
                            st.success(f"Venda #{venda_res.get('id')} realizada! Veículo #{obj_veiculo['id']} agora está marcado como VENDIDO.")
                            st.rerun()
                        else:
                            st.error(f"Erro: {r.json().get('detail', r.text)}")
                    except Exception as e:
                        st.error(f"Erro de conexão: {e}")

    # --- ABA 3: HISTÓRICO DE VENDAS ---
    with tab_historico_vendas:
        st.subheader("📋 Veículos Vendidos")
        
        veiculos_vendidos = [v for v in veiculos_todos if v.get("status") == "vendido"]
        if veiculos_vendidos:
            st.dataframe(veiculos_vendidos, use_container_width=True)
        else:
            st.info("Nenhum veículo com status 'vendido' encontrado no estoque atual.")

    # --- ABA 3: MANUTENÇÃO ---
    with tab_manut:
        st.subheader("Ordens de Manutenção")
        
        veiculos_aptos = [v for v in veiculos_todos if v.get("status") != "vendido"]
        
        if not veiculos_aptos:
            st.info("Nenhum veículo disponível para manutenção.")
        else:
            opcoes_m = {f"#{v['id']} - {v['marca']} {v['modelo']} (Status atual: {v['status']})": v for v in veiculos_aptos}
            v_manut_sel = st.selectbox("Selecione o Veículo para Manutenção", list(opcoes_m.keys()))
            obj_m = opcoes_m[v_manut_sel]

            with st.form("form_manutencao"):
                mecanico_id = st.number_input("ID do Mecânico (Funcionário)", min_value=1, value=3)
                descricao = st.text_area("Descrição do Serviço", value="Revisão geral e troca de óleo")
                custo = st.number_input("Custo Estimado (R$)", min_value=0.0, value=500.0, step=50.0)
                
                submit_m = st.form_submit_button("Registrar Ordem de Manutenção")
                if submit_m:
                    payload = {
                        "veiculo_id": int(obj_m["id"]),
                        "mecanico_id": int(mecanico_id),
                        "descricao": descricao,
                        "custo": float(custo)
                    }
                    try:
                        r = requests.post(f"{API_URL}/manutencoes", json=payload, timeout=30)
                        if r.status_code == 201:
                            m_res = r.json()
                            st.toast(f"Manutenção #{m_res.get('id')} aberta!", icon="🔧")
                            st.success(f"Ordem de Manutenção #{m_res.get('id')} aberta! Veículo #{obj_m['id']} atualizado para EM MANUTENÇÃO.")
                            st.rerun()
                        else:
                            st.error(f"Erro: {r.json().get('detail', r.text)}")
                    except Exception as e:
                        st.error(f"Erro de conexão: {e}")

    # --- ABA 4: FUNCIONÁRIOS E LOJAS ---
    with tab_equipe:
        st.subheader("Lojas e Funcionários")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏢 Lojas Cadastradas")
            try:
                r_lojas = requests.get(f"{API_URL}/lojas", timeout=30)
                if r_lojas.status_code == 200:
                    st.dataframe(r_lojas.json(), use_container_width=True)
                else:
                    st.info("Nenhuma loja cadastrada.")
            except Exception as e:
                st.error(f"Erro ao carregar lojas: {e}")
                
        with col2:
            st.markdown("#### 👥 Funcionários")
            try:
                r_funcs = requests.get(f"{API_URL}/funcionarios", timeout=30)
                if r_funcs.status_code == 200:
                    st.dataframe(r_funcs.json(), use_container_width=True)
                else:
                    st.info("Nenhum funcionário cadastrado.")
            except Exception as e:
                st.error(f"Erro ao carregar funcionários: {e}")
