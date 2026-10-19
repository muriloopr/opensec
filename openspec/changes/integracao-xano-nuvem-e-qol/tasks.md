# tasks: migracao definitiva para xano cloud

- [x] [task] Atualizar artefatos OpenSpec (`proposal.md` e `design.md`) especificando a remoção do SQLite e uso exclusivo do Xano Cloud.
- [x] [task] Refatorar `backend/main.py` para remover dependência do SQLite (`sqlite3`).
- [x] [task] Implementar requisições HTTP via `requests` nos endpoints do FastAPI apontando para `https://x8ki-letl-twmt.n7.xano.io/api:concessionaria-api`.
- [x] [task] Validar a comunicação e testes com a nova instância do Xano.
- [x] [task] Implementar melhorias de Qualidade de Vida (QoL) no frontend Streamlit com abas visíveis, cards de métricas, seleção dinâmica e notificações toast.
