# tarefas

## 1. backend de autenticação e gestão de usuários

* [x] 1.1 criar a tabela de usuários no /fastapi com id, email, senha_hash e data de criação.
* [x] 1.2 criar o endpoint post /auth/signup com validação de email duplicado e hash de senha, e confirmar o teste.
* [x] 1.3 criar o endpoint post /auth/login validando credenciais e emitindo token jwt/sessão, e confirmar funcionamento.

## 2. frontend em streamlit e telas de autenticação

* [x] 2.1 criar as telas/abas de login e cadastro no frontend/app.py.
* [x] 2.2 integrar os formulários de login e cadastro com a api do fastapi e salvar o token.
* [x] 2.3 rodar o teste completo do fluxo (cadastrar -> logar -> acessar telas protegidas da concessionária).