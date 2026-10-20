# readme - sistema de gestão para concessionárias

## 1. o problema

gerenciar uma rede de concessionárias ou uma loja de veículos costuma ser caótico quando a informação fica espalhada em planilhas, sistemas legados ou conversas soltas.

sem uma visão centralizada, a operação enfrenta gargalos comuns:

* **falta de visibilidade do estoque**: dificuldade para saber em qual loja física determinado carro está parado.
* **decisões sem dados**: ausência de kpis claros sobre faturamento, marcas mais vendidas e giro de estoque.
* **processos desconectados**: desalinhamento no acompanhamento de financiamentos com bancos, histórico de manutenção dos carros e vendas finalizadas por equipe.

## 2. público-alvo

o sistema foi pensado para simplificar a rotina de:

* **gestores e diretores de redes de concessionárias**: que precisam de dashboards executivos para acompanhar métricas de desempenho globais ou por unidade em tempo real.
* **equipes de vendas e gerentes de loja**: que precisam buscar carros rapidamente no estoque, filtrar por faixa de preço/ano e acompanhar o status de negociações.
* **equipes operacionais (mecanismos e administrativo)**: que fazem o controle das rotinas de manutenção dos veículos e o vínculo com instituições bancárias de financiamento.

---

## 3. escopo do mvp

o produto mínimo viável (mvp) foca nas funcionalidades essenciais para operacionalizar a gestão e dar visibilidade ao negócio:

### 📊 dashboard executivo

* cartões de kpis operacionais: total de veículos, carros disponíveis e valor investido em estoque.
* gráficos visuais com distribuição por marcas populares e status do veículo.

### 🚗 gestão e filtro de estoque

* busca rápida por marca ou modelo.
* filtros por faixa de preço, ano, status do veículo e loja física.
* visão unificada dos veículos à venda.

### 🏢 controle centralizado

* **lojas & vendedores**: seletor global para alternar a visão do sistema entre unidades específicas ou visualizar todas juntas.
* **clientes & bancos**: cadastro e relacionamento básico para apoio no fluxo de vendas e financiamento.
* **manutenção**: registro e acompanhamento de veículos em preparação ou reparo mecânico.

### ⚙️ infraestrutura e ux

* interface responsiva em streamlit integrada com backend (fastapi / xano).
* monitoramento em tempo real do status de conexão com a api na barra lateral.
