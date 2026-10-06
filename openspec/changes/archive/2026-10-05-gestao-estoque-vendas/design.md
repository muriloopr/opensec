# design: gestão de estoque e vendas

## contexto

o sistema utiliza um backend em fastapi integrado ao banco com frontend em streamlit. o detalhamento do contexto de negócio está no documento proposal.md.

## escopo

o que entra:

* centralizar os endpoints rest para veículos, lojas, funcionários, clientes, vendas e manutenções.
* garantir que validações de estoque e regras de transação fiquem exclusivamente no backend.
* manter o streamlit como uma camada visual leve, consumindo a api via requisições http.

o que fica de fora:

* autenticação complexa e suporte a múltiplos clientes (multi-tenant). o foco atual é consolidar o fluxo operacional principal.

## decisões arquiteturais

1. sqlite local para simular o xano
* decisão: estruturar as tabelas relacionais (veiculo, loja, funcionario, cliente, venda, manutencao) diretamente no sqlite.
* motivo: evita dependência de conexão externa com a nuvem do xano durante o desenvolvimento local.


2. validação estrita com fastapi e pydantic
* decisão: concentrar todas as checagens e tipos de dados no fastapi.
* motivo: impede o acoplamento de regras de negócio na interface em streamlit, mantendo o frontend puramente reativo.



## riscos e mitigações

* concorrência em vendas simultâneas: dois operadores tentando vender o mesmo veículo ao mesmo tempo.
* mitigação: verificar se o status do veículo é disponivel diretamente na transação do banco antes de registrar a venda.