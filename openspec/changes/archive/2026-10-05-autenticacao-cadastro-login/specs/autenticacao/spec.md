# spec delta

## objetivo

gerenciar o cadastro de usuários, autenticação por credenciais e emissão de tokens de sessão pra controlar o acesso ao sistema.

## novos requisitos

### requisito: cadastro de novos usuários

o sistema deve permitir cadastrar novos usuários com email e senha, garantindo que o email seja único.

#### cenário: cadastrar usuário com sucesso

* quando um novo usuário envia email e senha válidos
* então a conta é criada no banco com a senha protegida e retorna confirmação de sucesso

#### cenário: bloquear cadastro com email duplicado

* quando alguém tenta cadastrar uma conta usando um email que já existe
* então o sistema recusa o cadastro e avisa que o email já está em uso

### requisito: autenticação e login

o sistema deve autenticar os usuários com credenciais válidas e gerar um token de sessão (jwt).

#### cenário: logar com dados corretos

* quando o usuário envia email e senha certos na rota de login
* então o sistema valida os dados e retorna um token de acesso

#### cenário: recusar login com senha errada

* quando o usuário digita a senha errada pra um email existente
* então o sistema nega o acesso e avisa que as credenciais são inválidas

### requisito: telas de autenticação no frontend

o frontend em streamlit deve ter telas de cadastro e login, controlando o estado da sessão.

#### cenário: fazer login na interface

* quando o usuário não logado acessa o app e preenche o formulário de login
* então o token de acesso é salvo na sessão e a tela principal é liberada