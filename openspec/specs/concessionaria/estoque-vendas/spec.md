# concessionaria/estoque-vendas Specification

## Purpose
Gerencia o catálogo de veículos, o estoque por loja e o registro de operações de vendas e ordens de manutenção mecânica na concessionária.

## Requirements

### Requirement: Gerenciamento de Estoque de Veículos
O sistema SHALL permitir o cadastro e consulta de veículos com controle de status (`disponivel`, `vendido`, `em_manutencao`) vinculados a uma loja específica.

#### Scenario: Cadastrar veículo com status disponível
- **WHEN** um novo veículo é cadastrado com preço, ano, marca, modelo e loja associada
- **THEN** o veículo é armazenado com status inicial 'disponivel' e retornado com ID gerado

#### Scenario: Filtrar veículos por status
- **WHEN** o cliente ou operador solicita a listagem de veículos filtrando por status
- **THEN** o sistema retorna apenas os veículos correspondentes ao status solicitado

### Requirement: Registro Seguro de Vendas
O sistema SHALL registrar vendas de veículos apenas quando o veículo estiver com status 'disponivel', atualizando automaticamente o status do veículo para 'vendido'.

#### Scenario: Efetuar venda de veículo disponível
- **WHEN** uma venda é registrada informando veículo disponível, cliente, vendedor e tipo de pagamento
- **THEN** a venda é registrada no sistema e o status do veículo é alterado para 'vendido'

#### Scenario: Impedir venda de veículo indisponível
- **WHEN** uma tentativa de venda é feita para um veículo já vendido ou em manutenção
- **THEN** o sistema rejeita a operação com erro descritivo

### Requirement: Registro de Ordens de Manutenção
O sistema SHALL registrar serviços de manutenção mecânica associados a um veículo, alterando o status do veículo para 'em_manutencao'.

#### Scenario: Registrar manutenção em veículo
- **WHEN** uma ordem de manutenção é iniciada com descrição, custo e mecânico responsável
- **THEN** a manutenção é registrada e o status do veículo é atualizado para 'em_manutencao'
