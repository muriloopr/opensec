# design: autenticação, cadastro e login

## contexto

o sistema roda com backend em fastapi, banco sqlite e frontend em streamlit. o motivo da mudança tá detalhado no arquivo proposal.md.

## escopo

o que entra:

* criar as rotas /auth/signup e /auth/login com hash seguro de senha (bcrypt) e geração de token jwt.
* conectar as telas de login e cadastro no streamlit pra guardar o estado da sessão.

o que fica de fora:

* login social com provedores externos (google, github) por enquanto.

## decisões arquiteturais

1. uso de jwt para autenticação
* decisão: usar tokens jwt pra validar o acesso nas rotas protegidas.
* motivo: permite autenticar as requisições de forma simples entre o frontend e a api.


2. hash de senhas com bcrypt
* decisão: criptografar as senhas com bcrypt antes de salvar no banco.
* motivo: garante segurança no armazenamento local e evita guardar senhas em texto puro.



## riscos e mitigações

* perda de sessão ao dar refresh no streamlit: a página pode recarregar e perder o estado do usuário.
* mitigação: salvar o token de acesso no st.session_state pra manter a navegação autenticada.