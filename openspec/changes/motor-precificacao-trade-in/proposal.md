# Proposta: Motor de Precificação Dinâmica & Trade-In com Inteligência de Margem

## 1. Visão Geral da Feature e Valor de Negócio

### Contexto
No modelo tradicional de concessionárias, veículos retidos por longos períodos no pátio acumulam custos ocultos significativos (custo de oportunidade do capital imobilizado, taxa de depreciação de mercado e seguro de pátio). Paralelamente, negociações envolvendo a troca de veículos usados (*Trade-In*) frequentemente sofrem com a falta de visibilidade em tempo real sobre a margem de contribuição consolidada da transação, gerando vendas com margem líquida ilusória. Por fim, a venda do veículo isoladamente não maximiza o *Lifetime Value* (LTV) do cliente, perdendo receitas financeiras e de pós-venda.

### Objetivo
Implementar um **Motor de Precificação Dinâmica & Trade-In com Inteligência de Margem** para transformar o inventário da concessionária em um ativo de alto giro e liquidez, garantindo:
1. **Controle de Custo de Pátio (Holding Cost):** Monitoramento contínuo da perda diária de valor por veículo e sugestão proativa de reajustes automáticos para estoques com mais de 30 dias.
2. **Avaliador de Trade-In Inteligente:** Cálculo preciso da oferta ótima de compra do usado baseado na FIPE e despesas de recondicionamento, exibindo instantaneamente a margem combinada da operação ao vendedor.
3. **Simulador de Combos Financiamento + Manutenção:** Maximização do ticket médio e LTV mediante empacotamento de planos de manutenção preventiva (1 ou 2 anos) parcelados no fluxo do financiamento bancário.

### Impacto e Métricas de Sucesso
* **Redução no DSI (Days Sales of Inventory):** Redução de 25% no tempo médio de permanência dos carros em estoque.
* **Garantia de Margem Mínima:** Eliminação de negociações de *Trade-In* com margem combinada negativa ou inferior a 8%.
* **Incremento de LTV e Receita de Oficina:** Conversão estimada de 35% das vendas financiadas em combos de manutenção pré-paga, garantindo receita futura e comissões bancárias adicionais.

---

## 2. Casos de Uso e Fluxos Principais (User Stories)

### UC01 - Monitoramento e Precificação Dinâmica do Estoque de Pátio
* **Ator Principal:** Gerente de Pátio / Diretor Comercial.
* **User Story:**
  > *Como gerente da concessionária, quero acompanhar em tempo real o custo diário de carregar cada veículo em estoque e receber alertas quando um veículo ultrapassar 30 dias parado, para que eu possa aplicar sugestões de reajuste de preço e acelerar o giro antes que o veículo entre em depreciação crítica.*
* **Fluxo Principal:**
  1. O sistema calcula diariamente o custo de carregar o veículo (capital + depreciação + seguro).
  2. Ao atingir > 30 dias de pátio, o veículo entra em estado de `Alerta de Giro (Aging Stock)`.
  3. O gerente acessa o painel de precificação dinâmica e visualiza os veículos estagnados, o custo acumulado e a sugestão automática de desconto ideal.
  4. O gerente clica em "Aplicar Reajuste Sugerido", atualizando o preço público do veículo e notificando o time de vendas.

### UC02 - Avaliador de Trade-In Inteligente com Margem Combinada
* **Ator Principal:** Vendedor / Avaliador de Usados.
* **User Story:**
  > *Como vendedor, quero lançar os dados de um seminovo oferecido na troca (marca, modelo, ano, km, estado) ao fechar uma venda, para que o sistema me sugira a oferta ideal de captação e exiba a margem líquida combinada da transação em tempo real.*
* **Fluxo Principal:**
  1. O vendedor seleciona o veículo do estoque pretendido pelo cliente.
  2. O cliente oferece um veículo usado como parte do pagamento.
  3. O vendedor preenche os dados do seminovo e despesas previstas de revisão/funilaria.
  4. O sistema consulta a tabela de referência (FIPE) e parâmetros da loja, sugerindo a faixa ideal de oferta (Mínima / Ideal / Máxima).
  5. O vendedor informa o valor negociado com o cliente.
  6. O sistema exibe em tempo real:
     * Lucro bruto do carro novo/estoque.
     * Desconto/Overallowance concedido na troca.
     * Margem futura esperada do veículo usado.
     * **Margem Combinada da Operação** (em R$ e em %).
  7. Se a margem combinada for inferior ao limite de segurança (8%), o sistema bloqueia o fechamento automático e solicita alçada de liberação gerencial.

### UC03 - Simulador de Financiamento com Combos de Revisão
* **Ator Principal:** Consultor de Vendas / Operador de F&I (Finance & Insurance).
* **User Story:**
  > *Como consultor comercial, quero apresentar opções de financiamento que embutem revisões programadas na parcela, para demonstrar ao cliente economia no pós-venda enquanto aumento a margem e o LTV da transação.*
* **Fluxo Principal:**
  1. O operador informa o saldo devedor do veículo e define prazo (ex: 36x ou 48x) e taxa bancária.
  2. O sistema lista os pacotes de combo disponíveis (ex: "Plano Prata: 2 Anos de Revisão Garantida").
  3. Ao selecionar o combo, o sistema recalcula a tabela Price, comparando:
     * Parcela Convencional (somente carro).
     * Parcela com Combo Integrado (carro + revisões).
     * Diferença residual por mês (ex: "+ R$ 42,50/mês").
     * Economia total do cliente vs. revisões avulsas de balcão.
  4. Ao fechar o combo, o contrato de venda vincula o pacote, programando as ordens de serviço futuras no sistema de pós-venda.

---

## 3. Regras de Negócio Detalhadas

### 3.1 Fórmula do Custo de Carregar o Veículo (Holding Cost)
O custo diário de carregar um veículo é composto por três vetores financeiros:
1. **Custo de Oportunidade do Capital:** Taxa base anual ($i_{capital} = 12.0\%$ a.a. default).
2. **Depreciação de Mercado:** Curva anual de desvalorização ($i_{deprec} = 15.0\%$ a.a. default).
3. **Seguro e Segurança de Pátio:** Taxa de cobertura de pátio ($i_{seguro} = 1.2\%$ a.a. default).

**Taxa Composta Diária:**
$$i_{diaria} = \frac{i_{capital} + i_{deprec} + i_{seguro}}{365} = \frac{0.12 + 0.15 + 0.012}{365} \approx 0.0007726 \text{ (0,0773\% ao dia)}$$

**Custo Acumulado de Pátio:**
$$Custo\_Patio(dias) = Custo\_Aquisicao \times i_{diaria} \times dias\_em\_estoque$$

*Exemplo Prático:*
Para um veículo adquirido por R$ 80.000,00 parado há 40 dias:
* Custo Diário: $80.000 \times 0.0007726 \approx R\$\ 61,81/\text{dia}$
* Custo Acumulado (40 dias): $61,81 \times 40 = R\$\ 2.472,40$

### 3.2 Gatilho de 30 Dias e Sugestão de Reajuste Automático
* **Gatilho de Envelhecimento (Aging):**
  * `dias_estoque <= 30`: Status `NORMAL` (Verde).
  * `31 <= dias_estoque <= 45`: Status `ALERTA_AMARELO` (Atenção - risco de queima de margem).
  * `dias_estoque > 45`: Status `ALERTA_VERMELHO` (Crítico - imobilização prolongada).
* **Cálculo da Sugestão de Reajuste de Preço:**
  * **Faixa 31-45 dias:**
    $$Desconto\_Sugerido = \min(Preco\_Atual \times 0.04, Custo\_Acumulado\_Patio)$$
    $$Novo\_Preco\_Sugerido = Preco\_Atual - Desconto\_Sugerido$$
  * **Faixa > 45 dias:**
    $$Desconto\_Sugerido = \min(Preco\_Atual \times 0.07, Custo\_Acumulado\_Patio \times 1.25)$$
    $$Novo\_Preco\_Sugerido = Preco\_Atual - Desconto\_Sugerido$$
  * **Trava de Segurança:** O $Novo\_Preco\_Sugerido$ nunca poderá ser inferior a $Custo\_Aquisicao \times 1.02$ (preservando margem bruta mínima de 2% do valor de custo).

### 3.3 Avaliador de Trade-In e Cálculo de Margem Combinada
A transação de troca é modelada com base em duas pernas operacionais:

1. **Perna 1: Veículo do Estoque (Novo ou Usado Vendido)**
   $$Lucro\_Estoque = Preco\_Venda\_Estoque - Custo\_Aquisicao\_Estoque$$

2. **Perna 2: Veículo Usado Recebido na Troca (Trade-In)**
   * **Oferta Ideal de Compra:**
     $$Oferta\_Ideal = FIPE_{referencia} \times (1 - Margem\_Alvo) - Custo\_Recondicionamento$$
     *(Onde $Margem\_Alvo = 15\%$ para cobrir risco e custo operacional de revenda).*
   * **Overallowance (Sobrepreço na Entrada):**
     $$Overallowance = \max(0, Valor\_Pago\_Usado - Oferta\_Ideal)$$
   * **Margem Futura Projetada do Usado:**
     $$Margem\_Futura = FIPE_{referencia} - (Valor\_Pago\_Usado + Custo\_Recondicionamento)$$

3. **Margem Combinada Consolidada:**
   $$Margem\_Combinada\_R\$ = Lucro\_Estoque - Overallowance + \max(0, Margem\_Futura)$$
   $$Margem\_Combinada\_\% = \frac{Margem\_Combinada\_R\$}{Preco\_Venda\_Estoque + FIPE_{referencia}} \times 100$$
* **Regra de Bloqueio:** Se $Margem\_Combinada\_\% < 8.0\%$, o sistema exige justificativa formal e aprovação do perfil Gerencial.

### 3.4 Simulador de Financiamento e Combos com Manutenção
* **Tabela Price para Prestação Mensal:**
  $$PMT = PV \times \frac{i \times (1 + i)^n}{(1 + i)^n - 1}$$
  * $PV_{base} = Preco\_Venda - Valor\_Entrada$
  * $PV_{combo} = PV_{base} + Preco\_Pacote\_Manutencao$
  * $Acréscimo\_Mensal = PMT_{combo} - PMT_{base}$
* **Comissão de Intermediação e LTV:**
  * Comissão de F&I da concessionária: $Comissao\_Banco = PV \times 1.5\%$.
  * Margem Bruta Retida da Manutenção: $Preco\_Pacote - Custo\_Pecas\_MaoDeObra \approx 40\%$.
