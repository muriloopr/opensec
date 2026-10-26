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
    menu = st.sidebar.selectbox(
        "Escolha uma opção",
        [
            "📦 Estoque de Veículos",
            "📊 Precificação & Custo de Pátio",
            "🔄 Avaliador de Trade-In",
            "💳 Financiamento & Combos",
            "💰 Registrar Venda",
            "🔧 Ordens de Manutenção",
            "🏢 Funcionários e Lojas"
        ]
    )

    # ==================== 1. ESTOQUE DE VEÍCULOS ====================
    if menu == "📦 Estoque de Veículos":
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
            col1, col2 = st.columns(2)
            with col1:
                marca = st.text_input("Marca")
                modelo = st.text_input("Modelo")
                ano = st.number_input("Ano", min_value=1950, max_value=2030, value=2024)
            with col2:
                preco = st.number_input("Preço de Venda (R$)", min_value=0.0, value=50000.0)
                custo_aquisicao = st.number_input("Custo de Aquisição (R$)", min_value=0.0, value=42000.0)
                status_v = st.selectbox("Status Inicial", ["disponivel", "vendido", "em_manutencao"])
                loja_id = st.number_input("ID da Loja", min_value=1, value=1)
            
            submit = st.form_submit_button("Cadastrar Veículo")
            if submit:
                payload = {
                    "marca": marca,
                    "modelo": modelo,
                    "ano": int(ano),
                    "preco": float(preco),
                    "custo_aquisicao": float(custo_aquisicao),
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

    # ==================== 2. PRECIFICAÇÃO DINÂMICA & CUSTO DE PÁTIO ====================
    elif menu == "📊 Precificação & Custo de Pátio":
        st.header("📊 Motor de Precificação Dinâmica & Custo de Pátio")
        st.caption("Monitoramento diário de holding cost (custo de oportunidade, depreciação e seguro de pátio) com gatilhos de aging.")

        try:
            r = requests.get(f"{API_URL}/precificacao/patio/dashboard")
            if r.status_code == 200:
                data = r.json()
                
                # Cards de métricas principais
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Veículos em Pátio", data["total_veiculos_patio"])
                c2.metric("Custo Diário Total", f"R$ {data['custo_total_carregamento_dia']:,.2f}")
                c3.metric("Custo Acumulado Total", f"R$ {data['custo_acumulado_patio_total']:,.2f}")
                c4.metric(
                    "Em Alerta (> 30 dias)",
                    data["veiculos_alerta_contagem"],
                    delta=f"{data['veiculos_alerta_contagem']} em risco" if data['veiculos_alerta_contagem'] > 0 else "Estoque Otimizado",
                    delta_color="inverse"
                )

                st.divider()
                st.subheader("Veículos em Estoque e Sugestões de Giro")
                
                itens = data.get("itens", [])
                if itens:
                    st.dataframe(itens, use_container_width=True)

                    # Painel de Ação Rápida de Reajuste
                    st.divider()
                    st.subheader("⚡ Ação de Giro: Aplicar Reajuste Sugerido")
                    
                    opcoes_veiculos = {
                        f"ID {v['veiculo_id']} - {v['marca']} {v['modelo']} ({v['dias_em_estoque']} dias em pátio) | Preço: R$ {v['preco_atual']:,.2f} -> Sugerido: R$ {v['novo_preco_sugerido']:,.2f}": v
                        for v in itens if v["status_aging"] in ("ALERTA_AMARELO", "ALERTA_VERMELHO")
                    }

                    if opcoes_veiculos:
                        veiculo_selecionado_label = st.selectbox("Selecione um veículo em alerta para reajustar:", list(opcoes_veiculos.keys()))
                        veiculo_sel = opcoes_veiculos[veiculo_selecionado_label]

                        col_act1, col_act2 = st.columns(2)
                        with col_act1:
                            st.write(f"**Criticidade:** `{veiculo_sel['status_aging']}`")
                            st.write(f"**Desconto Sugerido:** R$ {veiculo_sel['desconto_sugerido']:,.2f}")
                            st.write(f"**Piso Mínimo de Segurança:** R$ {veiculo_sel['piso_seguranca']:,.2f}")
                        
                        with col_act2:
                            preco_ajustar = st.number_input(
                                "Confirmar Novo Preço (R$)",
                                min_value=float(veiculo_sel["piso_seguranca"]),
                                value=float(veiculo_sel["novo_preco_sugerido"])
                            )
                            motivo = st.text_input("Motivo da Alteração", value=f"Ajuste de aging {veiculo_sel['status_aging']}")
                            
                            if st.button("Aprovar e Atualizar Preço no Estoque"):
                                r_ajuste = requests.post(
                                    f"{API_URL}/precificacao/veiculos/{veiculo_sel['veiculo_id']}/aplicar-reajuste",
                                    json={"novo_preco": float(preco_ajustar), "motivo": motivo}
                                )
                                if r_ajuste.status_code == 200:
                                    st.success(r_ajuste.json()["mensagem"])
                                    st.rerun()
                                else:
                                    st.error(f"Erro: {r_ajuste.text}")
                    else:
                        st.success("🎉 Todos os veículos em estoque estão dentro do prazo ideal (< 30 dias). Nenhum reajuste necessário no momento!")
                else:
                    st.info("Nenhum veículo disponível no pátio.")
            else:
                st.error("Erro ao carregar dados do dashboard.")
        except Exception as e:
            st.error(f"Erro de conexão com o backend: {e}")

    # ==================== 3. AVALIADOR DE TRADE-IN ====================
    elif menu == "🔄 Avaliador de Trade-In":
        st.header("🔄 Avaliador de Trade-In Inteligente")
        st.caption("Cruzamento preditivo do seminovo de entrada com o histórico e margem consolidada da operação (Piso mínimo: 8%).")

        try:
            r_veiculos = requests.get(f"{API_URL}/veiculos?status=disponivel")
            veiculos_disp = r_veiculos.json() if r_veiculos.status_code == 200 else []
            
            if not veiculos_disp:
                st.warning("Não há veículos disponíveis no estoque para simular a troca.")
            else:
                opcoes_estoque = {
                    f"ID {v['id']} - {v['marca']} {v['modelo']} {v['ano']} (Preço: R$ {v['preco']:,.2f})": v["id"]
                    for v in veiculos_disp
                }

                col_v1, col_v2 = st.columns(2)
                with col_v1:
                    st.subheader("1. Carro Pretendido do Estoque")
                    veiculo_escolhido_label = st.selectbox("Veículo a ser Vendido", list(opcoes_estoque.keys()))
                    veiculo_desejado_id = opcoes_estoque[veiculo_escolhido_label]
                    
                    cliente_id = st.number_input("ID do Cliente", min_value=1, value=1)
                    vendedor_id = st.number_input("ID do Vendedor", min_value=1, value=2)

                with col_v2:
                    st.subheader("2. Seminovo Ofertado na Troca (Trade-In)")
                    marca_usado = st.text_input("Marca do Usado", value="Volkswagen")
                    modelo_usado = st.text_input("Modelo do Usado", value="Polo Highline")
                    ano_usado = st.number_input("Ano do Usado", min_value=1990, max_value=2030, value=2021)
                    km_usado = st.number_input("Quilometragem (km)", min_value=0, value=45000)
                    preco_fipe = st.number_input("Preço FIPE de Referência (R$)", min_value=0.0, value=75000.0)
                    custo_recond = st.number_input("Custo Previsto de Revisão/Funilaria (R$)", min_value=0.0, value=2500.0)
                    valor_proposto = st.number_input("Valor Ofertado ao Cliente pelo Usado (R$)", min_value=0.0, value=63000.0)

                if st.button("🔍 Calcular Margem da Operação Combinada", type="primary"):
                    payload_tradein = {
                        "veiculo_desejado_id": veiculo_desejado_id,
                        "cliente_id": int(cliente_id),
                        "vendedor_id": int(vendedor_id),
                        "marca_usado": marca_usado,
                        "modelo_usado": modelo_usado,
                        "ano_usado": int(ano_usado),
                        "km_usado": int(km_usado),
                        "preco_fipe": float(preco_fipe),
                        "custo_recondicionamento_est": float(custo_recond),
                        "valor_proposto_usado": float(valor_proposto)
                    }

                    r_aval = requests.post(f"{API_URL}/tradein/avaliar", json=payload_tradein)
                    if r_aval.status_code == 200:
                        res = r_aval.json()
                        st.session_state["ultima_avaliacao"] = res
                        st.session_state["payload_tradein_salvar"] = {
                            **payload_tradein,
                            "oferta_ideal_sugerida": res["usado_tradein"]["oferta_ideal_sugerida"],
                            "overallowance": res["usado_tradein"]["overallowance"],
                            "lucro_veiculo_novo": res["veiculo_desejado"]["lucro_bruto_novo"],
                            "margem_futura_usado": res["usado_tradein"]["margem_futura_usado"],
                            "margem_combinada_reais": res["analise_combinada"]["margem_combinada_reais"],
                            "margem_combinada_percentual": res["analise_combinada"]["margem_combinada_percentual"],
                            "status": "aprovado" if not res["analise_combinada"]["requer_alcada_gerente"] else "em_analise"
                        }
                    else:
                        st.error(f"Erro na avaliação: {r_aval.text}")

                if "ultima_avaliacao" in st.session_state:
                    res = st.session_state["ultima_avaliacao"]
                    st.divider()
                    st.subheader("📊 Resultado da Análise de Margem Integrada")

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Lucro do Carro Vendido", f"R$ {res['veiculo_desejado']['lucro_bruto_novo']:,.2f}")
                    m2.metric("Oferta Ideal Sugerida", f"R$ {res['usado_tradein']['oferta_ideal_sugerida']:,.2f}")
                    m3.metric("Overallowance Concedido", f"R$ {res['usado_tradein']['overallowance']:,.2f}")
                    m4.metric("Margem Futura do Usado", f"R$ {res['usado_tradein']['margem_futura_usado']:,.2f}")

                    st.markdown("---")
                    pct = res["analise_combinada"]["margem_combinada_percentual"]
                    reais = res["analise_combinada"]["margem_combinada_reais"]
                    
                    if not res["analise_combinada"]["requer_alcada_gerente"]:
                        st.success(f"### ✅ Margem Combinada Consolidada: R$ {reais:,.2f} ({pct}%)")
                        st.info(res["analise_combinada"]["recomendacao"])
                    else:
                        st.error(f"### ⚠️ Margem Combinada Abaixo do Piso: R$ {reais:,.2f} ({pct}%)")
                        st.warning(res["analise_combinada"]["recomendacao"])

                    if st.button("💾 Salvar Registro de Avaliação"):
                        payload_s = st.session_state.get("payload_tradein_salvar")
                        if payload_s:
                            r_salv = requests.post(f"{API_URL}/tradein/salvar", json=payload_s)
                            if r_salv.status_code == 201:
                                st.success("Avaliação registrada com sucesso no sistema!")
                            else:
                                st.error(f"Erro ao salvar: {r_salv.text}")

                st.divider()
                st.subheader("📜 Histórico de Avaliações Registradas")
                r_hist = requests.get(f"{API_URL}/tradein/historico")
                if r_hist.status_code == 200:
                    historico = r_hist.json()
                    if historico:
                        st.dataframe(historico, use_container_width=True)
                    else:
                        st.info("Nenhuma avaliação de trade-in registrada até o momento.")
        except Exception as e:
            st.error(f"Erro de conexão com o backend: {e}")

    # ==================== 4. SIMULADOR DE COMBOS FINANCIAMENTO + MANUTENÇÃO ====================
    elif menu == "💳 Financiamento & Combos":
        st.header("💳 Simulador de Combos: Financiamento + Manutenção Preventiva")
        st.caption("Aumente o LTV do cliente e a receita de F&I embutindo pacotes de revisão oficial suavemente na parcela bancária.")

        try:
            r_veiculos = requests.get(f"{API_URL}/veiculos?status=disponivel")
            r_pacotes = requests.get(f"{API_URL}/combos/pacotes")
            
            veiculos_disp = r_veiculos.json() if r_veiculos.status_code == 200 else []
            pacotes = r_pacotes.json() if r_pacotes.status_code == 200 else []

            if not veiculos_disp:
                st.warning("Não há veículos disponíveis no estoque para simulação.")
            else:
                opcoes_estoque = {
                    f"ID {v['id']} - {v['marca']} {v['modelo']} (R$ {v['preco']:,.2f})": v["id"]
                    for v in veiculos_disp
                }
                opcoes_pacotes = {
                    f"{p['nome']} - R$ {p['preco_tabela']:,.2f} ({p['duracao_meses']} meses / {p['qtd_revisoes']} revisões)": p["id"]
                    for p in pacotes
                }

                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    v_label = st.selectbox("Selecione o Veículo", list(opcoes_estoque.keys()))
                    v_id = opcoes_estoque[v_label]
                    entrada = st.number_input("Valor da Entrada (R$)", min_value=0.0, value=30000.0, step=1000.0)
                    prazo = st.slider("Prazo de Financiamento (Meses)", min_value=12, max_value=60, value=48, step=12)

                with col_f2:
                    p_label = st.selectbox("Selecione o Pacote de Manutenção", list(opcoes_pacotes.keys()))
                    p_id = opcoes_pacotes[p_label]
                    taxa_juros = st.number_input("Taxa de Juros Mensal (% a.m.)", min_value=0.5, max_value=5.0, value=1.69, step=0.1)

                if st.button("🚀 Simular Comparativo de Financiamento", type="primary"):
                    payload_combo = {
                        "veiculo_id": v_id,
                        "valor_entrada": float(entrada),
                        "num_parcelas": int(prazo),
                        "taxa_juros_mensal": float(taxa_juros) / 100.0,
                        "pacote_manutencao_id": p_id
                    }
                    r_sim = requests.post(f"{API_URL}/combos/simular-financiamento", json=payload_combo)
                    if r_sim.status_code == 200:
                        sim = r_sim.json()
                        st.divider()
                        st.subheader("📈 Comparativo Lado a Lado")

                        col_trad, col_comb = st.columns(2)
                        
                        with col_trad:
                            st.info("### 1. Financiamento Convencional")
                            st.write(f"**Saldo Financiado:** R$ {sim['simulacao_tradicional']['saldo_financiado']:,.2f}")
                            st.metric("Parcela Mensal", f"R$ {sim['simulacao_tradicional']['parcela_mensal']:,.2f}")
                            st.write(f"**Total Pago:** R$ {sim['simulacao_tradicional']['total_pago']:,.2f}")
                            st.write(f"**Total de Juros:** R$ {sim['simulacao_tradicional']['total_juros']:,.2f}")

                        with col_comb:
                            st.success(f"### 2. Combo {sim['simulacao_combo']['pacote_nome']}")
                            st.write(f"**Saldo Financiado c/ Pacote:** R$ {sim['simulacao_combo']['saldo_financiado']:,.2f}")
                            st.metric(
                                "Parcela Mensal c/ Combo",
                                f"R$ {sim['simulacao_combo']['parcela_mensal']:,.2f}",
                                delta=f"+ R$ {sim['simulacao_combo']['diferenca_parcela_mensal']:,.2f}/mês",
                                delta_color="normal"
                            )
                            st.write(f"**Economia Estimada para o Cliente:** R$ {sim['simulacao_combo']['economia_cliente_estimada']:,.2f}")
                            st.write(f"**Comissão Extra de F&I para a Loja:** R$ {sim['simulacao_combo']['comissao_adicional_loja']:,.2f}")

                        st.markdown("---")
                        st.warning(f"💡 **Pitch Comercial para Fechamento:**\n\n_{sim['simulacao_combo']['pitch_venda']}_")
                    else:
                        st.error(f"Erro na simulação: {r_sim.text}")
        except Exception as e:
            st.error(f"Erro de conexão com o backend: {e}")

    # ==================== 5. REGISTRAR VENDA ====================
    elif menu == "💰 Registrar Venda":
        st.header("💰 Registrar Venda de Veículo")
        
        with st.form("form_venda"):
            veiculo_id = st.number_input("ID do Veículo", min_value=1, value=1)
            cliente_id = st.number_input("ID do Cliente", min_value=1, value=1)
            vendedor_id = st.number_input("ID do Vendedor (Funcionário)", min_value=1, value=2)
            valor = st.number_input("Valor da Venda (R$)", min_value=0.0, value=50000.0)
            tipo_pagamento = st.selectbox("Tipo de Pagamento", ["venda", "financiamento"])
            tradein_id = st.number_input("ID de Avaliação Trade-In (opcional, 0 se nenhuma)", min_value=0, value=0)
            pacote_id = st.number_input("ID de Pacote de Manutenção (opcional, 0 se nenhum)", min_value=0, value=0)
            
            submit_venda = st.form_submit_button("Efetuar Venda")
            if submit_venda:
                payload = {
                    "veiculo_id": int(veiculo_id),
                    "cliente_id": int(cliente_id),
                    "vendedor_id": int(vendedor_id),
                    "valor": float(valor),
                    "tipo_pagamento": tipo_pagamento,
                    "tradein_id": int(tradein_id) if tradein_id > 0 else None,
                    "pacote_manutencao_id": int(pacote_id) if pacote_id > 0 else None
                }
                try:
                    r = requests.post(f"{API_URL}/vendas", json=payload)
                    if r.status_code == 201:
                        venda_feita = r.json()
                        st.success(f"Venda registrada com sucesso! Lucro consolidado da operação: R$ {venda_feita.get('lucro_combinado', 0.0):,.2f}")
                    else:
                        st.error(f"Erro: {r.json().get('detail', r.text)}")
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")

    # ==================== 6. ORDENS DE MANUTENÇÃO ====================
    elif menu == "🔧 Ordens de Manutenção":
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

    # ==================== 7. FUNCIONÁRIOS E LOJAS ====================
    elif menu == "🏢 Funcionários e Lojas":
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
