# proposta: autenticação, cadastro e login

## por que

o sistema da concessionária precisa de autenticação pra gerenciar usuários, permitindo criar novas contas, fazer login seguro e gerar tokens de sessão (jwt) no backend em fastapi, além de telas simples de login e cadastro no frontend em streamlit.

## o que muda

* rotas de autenticação: criação dos endpoints /auth/signup e /auth/login no fastapi pra cadastro e login dos usuários.
* gestão de sessão e tokens: geração e validação de tokens jwt pra proteger o acesso às rotas da concessionária.
* telas no frontend: inclusão dos formulários e telas de login e cadastro no streamlit (frontend/app.py).

## funcionalidades

### novas funcionalidades

* autenticacao: controle de contas, cadastro, login e emissão de tokens de sessão.

### funcionalidades alteradas

* nenhuma especificação anterior precisa de alteração.

## impacto

* backend (backend/main.py): criação da tabela de usuários e rotas de autenticação.
* frontend (frontend/app.py): telas de login/cadastro e controle de estado da sessão.
* segurança: senhas salvas com hash seguro e uso de tokens de acesso.