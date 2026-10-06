# modelo de domínio: app concessionária

## conceitos e entidades principais

### 1. loja

unidade física da concessionária.

* atributos: id, nome, endereco, telefone, cnpj
* relacionamentos:
* tem vários vendedores (1:n)
* guarda vários carros no estoque (1:n)
* conta com vários mecânicos vinculados (1:n)



### 2. vendedor

profissional responsável pelas vendas na loja.

* atributos: id, nome, cpf, telefone, email, comissao, loja_id
* relacionamentos: vinculado a 1 loja e realiza várias vendas (1:n)

### 3. carro

veículo no estoque disponível pra venda ou em manutenção.

* atributos: id, marca, modelo, ano, placa, cor, preco, status, loja_id
* relacionamentos: pertence a 1 loja e pode se associar a vendas e serviços (1:n)

### 4. banco

instituição financeira que atua no financiamento dos veículos.

* atributos: id, nome, taxa_juros, telefone
* relacionamentos: oferece vários financiamentos (1:n)

### 5. cliente

comprador ou dono do veículo.

* atributos: id, nome, cpf, telefone, email, endereco
* relacionamentos: pode ter várias vendas (1:n) e financiamentos (1:n)

### 6. mecânico

profissional responsável pelos serviços de manutenção.

* atributos: id, nome, cpf, especialidade, loja_id
* relacionamentos: ligado a 1 loja e realiza vários serviços nos carros (1:n)