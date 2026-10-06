# spec delta

## objetivo

gerenciar o catálogo de veículos, o estoque de cada loja e o registro de vendas e ordens de manutenção mecânica da concessionária.

## novos requisitos

### requisito: gerenciamento de estoque de veículos

o sistema deve permitir cadastrar e consultar veículos com controle de status (disponivel, vendido, em_manutencao) vinculados a uma loja.

#### cenário: cadastrar veículo como disponível

* quando um novo veículo for cadastrado com preço, ano, marca, modelo e loja associada
* então o veículo é salvo com o status inicial disponivel e retorna com o id gerado

#### cenário: filtrar veículos por status

* quando for solicitada a lista de veículos filtrando pelo status
* então o sistema retorna apenas os veículos correspondentes ao filtro

### requisito: registro seguro de vendas

o sistema só deve registrar vendas quando o veículo estiver com o status disponivel, atualizando o status pra vendido logo em seguida.

#### cenário: vender veículo disponível

* quando uma venda for registrada informando veículo disponível, cliente, vendedor e forma de pagamento
* então a venda é salva no sistema e o status do veículo muda pra vendido

#### cenário: bloquear venda de veículo indisponível

* quando tentarem vender um veículo que já consta como vendido ou em manutenção
* então o sistema recusa a operação e exibe uma mensagem de erro

### requisito: registro de ordens de manutenção

o sistema deve registrar serviços de manutenção associados a um veículo e alterar o status dele pra em_manutencao.

#### cenário: registrar manutenção

* quando uma ordem de manutenção for criada com descrição, custo e mecânico responsável
* então a manutenção é salva e o status do veículo é atualizado pra em_manutencao