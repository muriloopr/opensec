# autenticacao Specification

## Purpose
Gerencia o registo de utilizadores, autenticação por credenciais e emissão de tokens de sessão seguros para controle de acesso no sistema.

## Requirements

### Requirement: Registo de Novos Utilizadores
O sistema SHALL permitir o cadastro de novos utilizadores com email, senha e dados de perfil, garantindo validação de unicidade.

#### Scenario: Cadastrar utilizador com sucesso
- **WHEN** um novo utilizador envia email e senha válidos no endpoint de registo
- **THEN** a conta é criada no banco de dados com senha encriptada e retorna confirmação de sucesso

#### Scenario: Impedir registo com email duplicado
- **WHEN** um utilizador tenta registar uma conta com um email já existente
- **THEN** o sistema rejeita o registo com erro descritivo de duplicidade

### Requirement: Autenticação e Login de Utilizadores
O sistema SHALL autenticar utilizadores através de credenciais válidas e emitir um token de sessão/JWT.

#### Scenario: Autenticar utilizador com credenciais corretas
- **WHEN** o utilizador envia email e senha corretos para o endpoint de login
- **THEN** o sistema valida as credenciais e retorna um token de acesso válido

#### Scenario: Rejeitar login com senha incorreta
- **WHEN** o utilizador envia uma senha incorreta para um email existente
- **THEN** o sistema rejeita a autenticação com erro de credenciais inválidas

### Requirement: Telas de Autenticação no Frontend
O frontend Streamlit SHALL fornecer interfaces dedicadas para Registo e Login de utilizadores, gerenciando o estado da sessão.

#### Scenario: Visualizar tela de login e efetuar autenticação
- **WHEN** o utilizador não autenticado acede à aplicação e preenche o formulário de login
- **THEN** o token de acesso é armazenado na sessão e a interface principal é exibida
