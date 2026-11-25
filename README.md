# nassauTickets

Sistema de Controle de Atendimento para Laboratório de Análises Clínicas.  
Projeto final das disciplinas **Back End Frameworks** (Prof. Eduardo Hernandes) e **Front End** (Prof. João Ferreira), UNINASSAU, semestre 2026.2.

**Equipe:** [PREENCHER nome da equipe]

## Membros

| Nome             | Matrícula | Papel                    |
| ---------------- | --------- | ------------------------ |
| Rodrigo Nunes    | 01777171  | Scrum Master             |
| Ericlys Severino | 01656023  | Documentador             |
| Othon Henrique   | 01809897  | Desenvolvedor            |
| Marcio José      | 01813686  | Desenvolvedor (back end) |
| Daniel Dantas    | 01254056  | Testador                 |

## Descrição

O *nassauTickets* é uma solução digital projetada para gerenciar o fluxo completo de atendimento ao usuário por meio de um sistema automatizado de tickets (chamados). A aplicação gerencia desde o momento em que o cliente emite uma senha de forma anônima em um totem de autoatendimento, passando pela triagem em fila com algoritmos estritos de intercalação e priorização, até a chamada no painel central e a consolidação dos dados em relatórios de auditoria e desempenho gerencial.

## Objetivo

Consolidar os conhecimentos práticos em engenharia de software e desenvolvimento web através da criação de um ecossistema integrado (Frontend, Backend e Banco de Dados). O sistema visa otimizar o tempo de espera no atendimento laboratorial, mitigar problemas clássicos de concorrência de chamadas simultâneas, e fornecer métricas precisas sobre a eficiência da operação de atendimento.

## Tecnologias utilizadas

| Camada         | Tecnologia                                                                                                                                                           |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Back end       | Python 3.12+ (desenvolvido em 3.14), Flask, flask-smorest (OpenAPI/Swagger), Flask-SQLAlchemy, Flask-Migrate (Alembic), Flask-JWT-Extended, argon2-cffi, Marshmallow |
| Banco de dados | MySQL 8.0 (Docker)                                                                                                                                                   |
| Testes         | pytest (SQLite em memória)                                                                                                                                           |
| Front end      | React 19 (JavaScript/JSX, Hooks, Context API) + Vite                                                                                                                 |

## Informações sobre as branches

- **main**: código estável e documentação.
- **dev**: desenvolvimento. Tudo entra nela e depois é unificado na main (merge).

## Estrutura do repositório

nassauTickets/

├── backend/

│   ├── app/

│   │   ├── routers/        # blueprints (só recebem e respondem)

│   │   ├── services/       # regras de negócio

│   │   ├── repositories/   # acesso ao banco

│   │   ├── models/         # tabelas (SQLAlchemy)

│   │   ├── schemas/        # validação e serialização

│   │   └── core/           # config, exceções, segurança

│   ├── database/           # migrations e seed

│   ├── tests/              # testes automatizados

│   ├── Dockerfile

│   ├── requirements.txt

│   ├── .env.example

│   └── wsgi.py

├── frontend/

│   ├── Dockerfile

│   └── ...

├── docs/                   # requisitos, diagramas, decisões

├── docker-compose.yml      # sobe tudo de uma vez

└── README.md


---

## Como executar (recomendado – Docker)

### Pré-requisitos
- Docker Desktop instalado e **ligado**

### Passos

```bash
git clone https://github.com/Rodrigonpp/nassauTickets
cd nassauTickets
git checkout dev

# Copia o arquivo de ambiente
cp backend/.env.example backend/.env