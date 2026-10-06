# tarefas

## 1. validação do backend e endpoints de estoque e vendas

* [x] 1.1 testar e validar o endpoint get /veiculos com filtro de status no fastapi pra ver se os dados estão vindo certos.
* [x] 1.2 testar o post /vendas pra garantir que só venda veículo com status disponivel e atualize pra vendido.
* [x] 1.3 testar o post /manutencoes pra registrar ordem de serviço e mudar o status do veículo pra em_manutencao.

## 2. ajuste do frontend e testes de integração

* [x] 2.1 checar a interface no streamlit (frontend/app.py) na parte de estoque, cadastro e registro de vendas/manutenções.
* [x] 2.2 rodar o teste do fluxo completo (cadastrar -> listar -> vender ou mandar pra manutenção) e confirmar que tá funcionando.