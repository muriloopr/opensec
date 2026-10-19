# visão geral do projeto: app concessionária

## 1. visão geral

sistema web pra gerenciar a operação do dia a dia de uma rede de concessionárias.

## 2. problema

centralizar a gestão de lojas, veículos, vendas, financiamentos e manutenções num lugar só, evitando bagunça no estoque e processo manual.
## 3. objetivos

cuidar de todo o ciclo de vida dos carros na loja, desde o cadastro até a venda, financiamento e manutenção.

## 4. escopo e funcionalidades

* cadastros e listagens: lojas, vendedores, mecânicos, clientes, carros e bancos.
* operações: registro de vendas, acompanhamento de financiamentos e ordens de manutenção.
* dashboard: visão rápida dos indicadores da concessionária.

## 5. arquitetura e tecnologias

* frontend: streamlit
* backend: fastapi
* banco de dados / regras: xano (xanoscript)

## 6. princípios de desenvolvimento

desenvolvimento guiado por specs usando o openspec, entregando partes pequenas, testáveis e em etapas.