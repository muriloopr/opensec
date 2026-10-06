## 1. princípios gerais

* tocar o projeto de forma incremental usando o fluxo do openspec.
* sempre checar a documentação na pasta docs/ antes de sugerir ou fazer mudanças grandes.
* seguir a arquitetura e a stack técnica combinada.
* escrever todo o código, documentação e arquivos em português do brasil.

## 2. tecnologias do projeto

* backend: python + fastapi
* frontend: python + streamlit
* banco de dados / regras: xano (xanoscript)

## 3. diretrizes de código e arquitetura

* o frontend em streamlit só deve consumir as apis do fastapi ou os endpoints do xano.
* validações e regras de negócio ficam todas no backend ou no xano, mantendo a tela limpa.
* evitar código duplicado e mexer em coisas fora do escopo da tarefa atual.