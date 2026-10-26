# concessionaria/precificacao-tradein Specification

## Purpose
Gerencia o cálculo dinâmico de custo de carregamento de pátio (holding cost), alertas de estagnação de veículos (> 30 dias), avaliação preditiva de usados em trade-in com cálculo em tempo real de margem combinada e simulação de combos de financiamento bancário com pacotes de manutenção integrada.

## Requirements

### Requirement: Cálculo de Custo Diário de Pátio e Alertas de Aging
O sistema SHALL calcular o custo financeiro diário de carregamento para cada veículo em estoque e alertar os gestores quando o período de pátio for superior a 30 dias, recomendando sugestões de reajuste automático de preço.

#### Scenario: Veículo com menos de 30 dias em estoque
- **WHEN** o veículo estiver em estoque há 30 dias ou menos
- **THEN** o sistema exibe o custo diário acumulado e mantém o status como 'NORMAL' sem sugestão de desconto

#### Scenario: Alerta amarelo para veículo entre 31 e 45 dias
- **WHEN** o veículo atingir entre 31 e 45 dias em estoque
- **THEN** o sistema atribui status 'ALERTA_AMARELO' e sugere um desconto de giro de até 4% limitado ao custo de pátio

#### Scenario: Alerta vermelho para veículo estagnado há mais de 45 dias
- **WHEN** o veículo ultrapassar 45 dias em estoque
- **THEN** o sistema atribui status 'ALERTA_VERMELHO' e sugere corte de preço agressivo de até 7%, respeitando o piso mínimo de 2% sobre o custo de aquisição

---

### Requirement: Avaliação de Trade-In e Inteligência de Margem Combinada
O sistema SHALL calcular a oferta ideal para veículos usados ofertados como entrada com base na FIPE e despesas de recondicionamento, computando a margem combinada da transação em tempo real.

#### Scenario: Oferta de entrada dentro do piso de margem combinada
- **WHEN** o vendedor informa os dados do usado e o valor acordado com o cliente resulta em margem combinada >= 8%
- **THEN** a operação é marcada como 'APROVADO' e exibe o detalhamento do lucro do veículo em estoque, eventual overallowance e margem futura

#### Scenario: Bloqueio por margem combinada abaixo do limite
- **WHEN** o valor acordado para o veículo de troca reduzir a margem combinada para menos de 8%
- **THEN** o sistema sinaliza 'REQUER_ALCADA_GERENCIAL', bloqueando a finalização automática sem liberação de gerente

---

### Requirement: Simulador de Financiamento e Combos com Pacote de Manutenção
O sistema SHALL simular parcelas pela Tabela Price permitindo agregar pacotes de serviços preventivos de oficina ao montante financiado, apresentando comparativo de custo-benefício e acréscimo mensal suave.

#### Scenario: Simular financiamento com combo de manutenção
- **WHEN** o cliente ou operador seleciona um pacote de manutenção para agregar ao financiamento
- **THEN** o sistema recalcula a prestação mensal, exibindo lado a lado a parcela comum, a parcela com combo, a diferença mensal e a economia estimada no pós-venda
