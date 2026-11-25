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

O _nassauTickets_ é uma solução digital projetada para gerenciar o fluxo completo de atendimento ao usuário por meio de um sistema automatizado de tickets (chamados). A aplicação gerencia desde o momento em que o cliente emite uma senha de forma anônima em um totem de autoatendimento, passando pela triagem em fila com algoritmos estritos de intercalação e priorização, até a chamada no painel central e a consolidação dos dados em relatórios de auditoria e desempenho gerencial.

## Objetivo

Consolidar os conhecimentos práticos em engenharia de software e desenvolvimento web através da criação de um ecossistema integrado (Frontend, Backend e Banco de Dados). O sistema visa otimizar o tempo de espera no atendimento laboratorial, mitigar problemas clássicos de concorrência de chamadas simultâneas, e fornecer métricas precisas sobre a eficiência da operação de atendimento.

## Tecnologias utilizadas

| Camada         | Tecnologia                                                                                                                                                           |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Back end       | Python 3.12+ (desenvolvido em 3.14), Flask, flask-smorest (OpenAPI/Swagger), Flask-SQLAlchemy, Flask-Migrate (Alembic), Flask-JWT-Extended, argon2-cffi, Marshmallow |
| Banco de dados | MySQL 8.0 (Docker)                                                                                                                                                   |
| Testes         | pytest (SQLite em memória)                                                                                                                                           |
| Front end      | React 19 (JavaScript/JSX, Hooks, Context API)                                                                                                                        |

## Informações sobre as branches

- _main_: código estável e documentação.
- _dev_: desenvolvimento. Tudo entra nela e depois é unificado na main (merge).

## Estrutura do repositório

```
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
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── .env.example
│   └── wsgi.py
├── docs/                   # requisitos, diagramas, decisões
└── frontend/
```

## Back end: como executar

### Pré-requisitos

- Python 3.12 ou superior
- Docker Desktop (aberto, com o engine rodando)
- Git

### Instalação e execução (PowerShell)

Um comando por vez.

```powershell
git clone https://github.com/Rodrigonpp/nassauTickets
cd nassauTickets
git checkout dev
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite o `.env` (veja a seção de variáveis) e depois:

```powershell
docker compose up -d
docker compose ps
```

Aguarde o status **healthy** (até 90 segundos na primeira vez). Então:

```powershell
flask --app wsgi db upgrade -d database/migrations
python -m database.seed
flask --app wsgi run --debug
```

O banco e o usuário são criados pelo Docker a partir do `.env`; as tabelas vêm das migrations; os dados iniciais, do seed.

- Documentação interativa (Swagger): http://localhost:5000/docs
- Health check: http://localhost:5000/api/v1/health

### Variáveis de ambiente (`.env`)

| Variável           | Exemplo                 | Descrição                                                    |
| ------------------ | ----------------------- | ------------------------------------------------------------ |
| DB_HOST            | localhost               | Host do MySQL                                                |
| DB_PORT            | 3306                    | Porta                                                        |
| DB_NAME            | nassau_tickets          | Nome do banco                                                |
| DB_USER            | nassau                  | Usuário                                                      |
| DB_PASSWORD        | (sua senha)             | Senha do usuário                                             |
| DB_ROOT_PASSWORD   | (sua senha)             | Senha root do container                                      |
| JWT_SECRET         | (texto longo aleatório) | Chave de assinatura dos tokens                               |
| JWT_EXPIRE_MINUTES | 60                      | Validade do token                                            |
| EXPEDIENTE_LIVRE   | false                   | `true` desliga a trava das 07h às 17h (somente demonstração) |

Gerar um `JWT_SECRET`: `python -c "import secrets; print(secrets.token_hex(32))"`

### Usuários de teste (seed)

| Perfil    | Login                                              | Senha      |
| --------- | -------------------------------------------------- | ---------- |
| GESTOR    | gestor@nassau.com.br                               | Gestor@123 |
| ATENDENTE | usuario1@nassau.com.br ... usuario10@nassau.com.br | Atend@123  |

O seed também cria 10 guichês (1 a 10).

### Testes

```powershell
python -m pytest -v
```

Os testes usam SQLite em memória e não precisam do Docker.

Simulação de concorrência (MySQL no ar, seed aplicado, **API parada**; apaga as senhas do banco local):

```powershell
python -m tests.simular_concorrencia
```

Resultado esperado: 30 chamadas, 30 únicas, nenhuma duplicada.

## API (resumo)

Todas sob `/api/v1`. Documentação completa no Swagger.

| Método | Rota                                                          | Acesso          | Descrição                                    |
| ------ | ------------------------------------------------------------- | --------------- | -------------------------------------------- |
| GET    | /health                                                       | público         | Verifica API e banco                         |
| POST   | /auth/login                                                   | público         | Login, devolve JWT                           |
| POST   | /senhas                                                       | público (totem) | Emite senha `{"tipo":"SP\|SG\|SE"}`          |
| GET    | /painel                                                       | público         | 5 últimas senhas chamadas                    |
| POST   | /atendimentos/chamar-proximo                                  | ATENDENTE       | Chama a próxima `{"guiche_id":1}`            |
| POST   | /atendimentos/{id}/chamar-novamente                           | ATENDENTE       | Segunda chamada                              |
| POST   | /atendimentos/{id}/iniciar                                    | ATENDENTE       | Inicia o atendimento                         |
| POST   | /atendimentos/{id}/encerrar                                   | ATENDENTE       | Encerra o atendimento                        |
| POST   | /atendimentos/{id}/nao-compareceu                             | ATENDENTE       | Marca não comparecimento                     |
| GET    | /relatorios/resumo, /detalhado, /tm, /auditoria, /indicadores | GESTOR          | Aceitam `?data=AAAA-MM-DD` ou `?mes=AAAA-MM` |
| POST   | /admin/descartar-sobras                                       | GESTOR          | Descarta senhas que sobraram                 |
| POST   | /admin/usuarios                                               | GESTOR          | Cadastra usuário                             |

Rotas protegidas exigem o header `Authorization: Bearer <token>`. Erros seguem o formato `{"codigo": 403, "mensagem": "..."}`.

## Regras de negócio implementadas

- Senhas SP, SG e SE, emitidas sem login, numeração `YYMMDD-PPSQ` com sequencial por tipo e reinício diário.
- Alternância `[SP] -> [SE|SG] -> [SP] -> [SE|SG]`, com SE antes de SG e tratamento de filas vazias.
- Qualquer guichê atende qualquer tipo de senha.
- Expediente das 07h às 17h (fuso America/Recife) na emissão e na chamada.
- Máquina de estados com 7 estados, transições validadas e histórico em `senha_historico`.
- Duas chamadas sem comparecimento levam a NAO_COMPARECEU.
- Atendente com atendimento em andamento não chama outra senha.
- Descarte das sobras no fim do expediente (sem oitavo estado: campos `descartada_em` e `motivo_descarte`).
- TM simulado: SP 15 min (±5), SG 5 min (±3), SE 1 min (95%) ou 5 min (5%).
- Painel com as 5 últimas chamadas (nunca a próxima) e flag `ultima_chamada` para o áudio.
- Relatórios diário e mensal, auditoria e indicadores de desempenho (espera média, taxa de não comparecimento, taxa de descarte, atendimentos por guichê e por atendente).

## Concorrência

Estratégia em três camadas, na chamada da próxima senha:

1. `SELECT ... FOR UPDATE` na linha única da tabela `estado_fila`: serializa a decisão (necessário porque a alternância depende do estado anterior).
2. `FOR UPDATE SKIP LOCKED` na busca da senha.
3. `UNIQUE(senha_id)` em `atendimentos_auditoria`: o banco impede duas atribuições da mesma senha.

Evidência: `python -m tests.simular_concorrencia` (10 atendentes simultâneos, 30 senhas, 0 duplicadas).

## Segurança e LGPD

- Senhas com hash argon2; autenticação JWT; controle de acesso por perfil (ATENDENTE e GESTOR).
- O cliente é anônimo: nenhum dado pessoal é coletado, apenas a senha.
- Minimização e finalidade: guardamos só o necessário para a operação e a auditoria.
- Registro de acesso em `log_acesso` (tentativas de login, sem gravar a senha).
- Mensagem de login genérica, sem revelar se o usuário existe.
- Segredos fora do código (`.env` não é versionado).

## Disponibilidade e falhas

- `GET /health` retorna 503 com mensagem padronizada quando o banco está indisponível.
- O pool de conexões usa `pool_pre_ping` para descartar conexões quebradas.
- Comportamento esperado do front/painel com API ou banco fora: manter a última tela exibida, mostrar o aviso "Sistema temporariamente indisponível" e tentar novamente a cada poucos segundos.
- Backup: `docker compose exec db mysqldump -unassau -p<senha> nassau_tickets > backup.sql`.

## Integração com o front end

- Base da API: `http://localhost:5000/api/v1`. CORS liberado para `localhost` nas portas 5173, 4200 e 3000.
- Fluxo: login, guardar o token, enviar `Authorization: Bearer <token>`, chamar `chamar-proximo`, usar o `id` devolvido nos demais endpoints.
- O painel consulta `GET /painel` periodicamente; `ultima_chamada: true` indica tocar "Última chamada".
- Fora do horário de expediente, usar `EXPEDIENTE_LIVRE=true` no `.env` do back.

## Front end: como executar

Pré-requisitos: Node.js e Git.

```bash
cd frontend
npm install
npm run dev
```

Link do front: http://localhost:5173/

## Funcionalidades

**Implementadas:** tudo listado em "Regras de negócio implementadas", mais login, relatórios, cadastro de usuários e documentação OpenAPI.

**Não implementadas / limitações:**

- Descarte automático de ~5% das senhas: o serviço existe (`descarte_service`), mas não há agendamento automático.
- Descarte de fim de expediente é acionado pelo gestor (`POST /admin/descartar-sobras`), sem agendador.
- Sequencial limitado a 999 senhas por tipo por dia (formato `SQ` de 3 dígitos).
- Sem tela de recuperação de senha.

## Decisões de arquitetura

Camadas separadas (routers, services, repositories, models); `estado_fila` como ponto de bloqueio da concorrência; descarte sem oitavo estado; histórico de transições. Detalhes em `docs/`.

## Uso de IA generativa

Foi utilizada IA generativa (Claude, da Anthropic) como ferramenta de apoio na geração e revisão de código e documentação. A equipe revisou o material e é capaz de explicar o código produzido.
