# proposta: gestão de estoque e vendas

## por que

a aplicação da concessionária precisa de um fluxo operacional simples e integrado entre o backend em fastapi, o banco de dados simulando o xanoscript e o frontend em streamlit. isso serve para gerenciar o estoque, cadastrar lojas e funcionários, e registrar vendas e manutenções sem correr o risco de vender um veículo indisponível.

## o que muda

* gestão de veículos e estoque: validação direta dos status dos veículos (disponivel, vendido, em_manutencao).
* registro de vendas e manutenções: novas rotas e telas para registrar vendas e ordens de serviço com segurança.
* integração frontend-backend: interface do streamlit consumindo a api do fastapi com tratamento simples de erros e exibição correta dos dados.

## funcionalidades

### novas funcionalidades

* concessionaria/estoque-vendas: controle geral de veículos, estoque, lojas, funcionários, vendas e manutenções.

### funcionalidades alteradas

* nenhuma especificação anterior precisa de alteração estrutural.

## impacto

* backend (backend/main.py): validação de status dos veículos e fluxo de transações de venda e manutenção.
* frontend (frontend/app.py): melhoria na interface para tratar erros da api e exibir os dados.
* openspec: primeiro conjunto de especificações para organizar o desenvolvimento do projeto.