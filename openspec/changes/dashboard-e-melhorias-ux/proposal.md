proposta: dashboard executivo, barra lateral avançada e filtros de estoque
1. resumo
melhorar a experiência do usuário (ux) do frontend em streamlit com:

aba de dashboard executivo: kpis de faturamento, vendas por loja, marcas mais buscadas e gráficos interativos.

barra lateral avançada: seletor global de loja, status em tempo real da api xano e atalhos rápidos.

filtros de estoque: slider de preço, faixa de ano e busca por texto na aba de estoque.

2. motivação
hoje o app só tem listagens básicas e a navegação troca de aba de forma simples. criar um dashboard gerencial e filtros mais completos traz valor real pro negócio e deixa o sistema mais alinhado aos objetivos do project-overview.md.

3. escopo das alterações
criar a aba "dashboard" na navegação principal.

ajustar o frontend/app.py pra controlar a loja selecionada no estado global pela barra lateral.

montar os gráficos no streamlit usando os dados do backend (fastapi / xano).

colocar mais opções de filtro na aba de estoque.