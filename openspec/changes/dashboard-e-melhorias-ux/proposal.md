# Proposta: Dashboard Executivo, Barra Lateral Avançada e Filtros de Estoque

## 1. Resumo
Melhorar a experiência do usuário (UX) do frontend Streamlit adicionando:
1. **Aba de Dashboard Executivo**: KPIs de faturamento, vendas por loja, marcas mais populares e gráficos interativos.
2. **Barra Lateral Avançada**: Seletor global de loja, status de conexão da API Xano em tempo real e atalhos rápidos.
3. **Filtros Avançados de Estoque**: Slider de preço, faixa de ano e busca textual na aba de estoque.

## 2. Motivação
Atualmente o app possui listagens básicas e o menu é apenas uma troca de abas simples. Um dashboard gerencial e filtros robustos agregam valor real de negócio para o sistema de concessionária, alinhando-se aos objetivos do projeto especificados em `project-overview.md`.

## 3. Escopo da Mudança
- Adicionar aba "📊 Dashboard" no topo da navegação.
- Atualizar `frontend/app.py` para suportar estado global de loja selecionada na barra lateral.
- Implementar gráficos com Streamlit e dados vindos do backend FastAPI / Xano.
- Expandir filtros na aba de estoque de veículos.
