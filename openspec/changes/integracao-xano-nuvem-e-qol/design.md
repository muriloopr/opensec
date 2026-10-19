# design: migracao definitiva para xano cloud

## contexto
o backend FastAPI anteriormente utilizava SQLite para simular o comportamento do Xano. agora, a arquitetura passa a ser 100% dependente da nuvem Xano.

## decisões arquiteturais
1. **FastAPI como Proxy/Client HTTP:**
   - As rotas do FastAPI farão chamadas REST utilizando a biblioteca `requests` para a instância Xano: `https://x8ki-letl-twmt.n7.xano.io/api:concessionaria-api`.
2. **Remoção do SQLite:**
   - O arquivo `concessionaria.db` e as funções de criação de tabelas locais (`init_db`) serão descontinuados do código de execução principal.
