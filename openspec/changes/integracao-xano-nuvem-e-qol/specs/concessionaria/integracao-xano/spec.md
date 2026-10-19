# specs/concessionaria/integracao-xano/spec.md

## Purpose
Especifica a integração oficial da aplicação de concessionária com a instância do Xano na nuvem e as melhorias de qualidade de vida.

## Requirements

### Requirement: Conexão Exclusiva com Xano Cloud
O sistema SHALL comunicar-se exclusivamente com a API REST fornecida pelo Xano na nuvem (`https://x8ki-letl-twmt.n7.xano.io/api:concessionaria-api`), eliminando o uso de bancos de dados locais em SQLite para a operação em produção/homologação.

#### Scenario: Consultar veículos na nuvem Xano
- **WHEN** o usuário acessa a listagem de veículos
- **THEN** o sistema consome o endpoint `GET /veiculo` diretamente do Xano e exibe os registros

### Requirement: Melhorias de Qualidade de Vida (QoL)
O sistema SHALL prover feedback visual imediato e filtros avançados na interface Streamlit para agilizar a operação diária.

#### Scenario: Feedback visual em operações de venda e manutenção
- **WHEN** uma venda ou manutenção é registrada com sucesso
- **THEN** o sistema exibe um alerta toast ou success message destacando o ID da operação
