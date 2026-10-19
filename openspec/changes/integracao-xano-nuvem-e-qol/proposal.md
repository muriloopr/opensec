# proposal: migracao definitiva para xano cloud e remocao do sqlite

## resumo
migrar o sistema de concessionária de forma definitiva para utilizar a API do Xano na nuvem (`x8ki-letl-twmt`), removendo completamente o banco de dados SQLite local e fazendo o backend FastAPI atuar como cliente HTTP dos endpoints Xano.

## motivação
garantir que todas as operações e transações de negócio sejam executadas nativamente no workspace do Xano na nuvem (`Murilo's Workspace`, ID `154082`), eliminando qualquer simulação local.

## escopo
- **o que entra:**
  - remoção do driver `sqlite3` e funções de banco local em `backend/main.py`.
  - reescrita dos endpoints do FastAPI para encaminhar requisições (`GET`, `POST`) via HTTP (`requests`) para a Base URL do Xano (`https://x8ki-letl-twmt.n7.xano.io/api:concessionaria-api`).
  - atualização dos testes automatizados para mockar ou integrar com a API do Xano.
- **o que fica de fora:**
  - persistência em arquivos locais.
