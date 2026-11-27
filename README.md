# nassauTickets

Sistema de Controle de Atendimento para Laboratório de Análises Clínicas.
Projeto final das disciplinas **Back End Frameworks** (Prof. Eduardo Hernandes) e **Front End** (Prof. João Ferreira), UNINASSAU, semestre 2026.2.



## Membros

| Nome | Matrícula | Papel |
|---|---|---|
| Rodrigo Nunes | 01777171 | Scrum Master |
| Ericlys Severino | 01656023 | Documentador |
| Othon Henrique | 01809897 | Desenvolvedor |
| Marcio José | 01813686 | Desenvolvedor (back end) |
| Daniel Dantas | 01254056 | Testador |

## Descrição

O *nassauTickets* gerencia o fluxo completo de atendimento por senhas: o cliente emite uma senha de forma anônima em um totem, a senha entra em uma fila com regras de priorização e alternância, é chamada no painel e atendida em um guichê. Ao final, os dados alimentam relatórios de auditoria e indicadores de desempenho para o gestor.

## Objetivo

Consolidar conhecimentos de engenharia de software e desenvolvimento web em um sistema integrado (front end, back end e banco de dados), reduzindo o tempo de espera, tratando a concorrência de chamadas simultâneas e fornecendo métricas da operação.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Back end | Python 3.12+, Flask, flask-smorest (OpenAPI/Swagger), Flask-SQLAlchemy, Flask-Migrate (Alembic), Flask-JWT-Extended, argon2-cffi, Marshmallow |
| Banco de dados | MySQL 8.0 |
| Testes | pytest (SQLite em memória) |
| Front end | React 19 + Vite (servido por nginx no Docker) |
| Infraestrutura | Docker e Docker Compose |

## Branches

* `main`: código estável e documentação (versão de entrega, tag `v1.0-entrega`).
* `dev`: desenvolvimento; tudo entra nela e depois é unificado na `main`.

---

## Como executar (recomendado: Docker)

**Pré-requisito:** Docker Desktop instalado e aberto (engine rodando). Nada mais é necessário: não precisa instalar Python, Node nem MySQL.

Todos os comandos na **raiz** do repositório (PowerShell):

```powershell
git clone https://github.com/Rodrigonpp/nassauTickets
cd nassauTickets
git checkout main
docker compose up --build
```

Na primeira vez leva alguns minutos (baixa as imagens e faz o build). O compose sobe três serviços: MySQL, API (que executa as migrations e o seed automaticamente) e o front.

| Serviço | URL |
|---|---|
| Front end | http://127.0.0.1:5173 |
| API | http://127.0.0.1:5000/api/v1 |
| Swagger (documentação) | http://127.0.0.1:5000/docs |
| Health check | http://127.0.0.1:5000/api/v1/health |

### Demonstração fora do horário de expediente

A emissão e a chamada só funcionam entre 07h e 17h (regra do edital) e retornam 403 fora disso. Para demonstrar à noite:

```powershell
$env:EXPEDIENTE_LIVRE="true"
docker compose up --build
```

### Comandos úteis

```powershell
docker compose down          # parar
docker compose logs -f       # ver logs
docker compose down -v       # parar e apagar o banco (recomeçar do zero)
```

### Possíveis problemas

* **Porta ocupada:** o banco é exposto em `3307` (externamente) para evitar conflito com um MySQL local; a API o acessa internamente em `db:3306`. Se a 5000 ou a 5173 estiverem em uso, altere o lado esquerdo da porta no `docker-compose.yml`.
* **Banco "unhealthy" na primeira subida:** a inicialização do MySQL pode levar mais de um minuto; rode `docker compose up` novamente.
* **Valores padrão:** senhas e `JWT_SECRET` do compose são apenas para demonstração. Em uso real, devem vir de variáveis de ambiente.

## Execução manual (alternativa)

**Back end** (pasta `backend`, Python 3.12+):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
docker run -d --name nassau_mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root123 -e MYSQL_DATABASE=nassau_tickets -e MYSQL_USER=nassau -e MYSQL_PASSWORD=nassau123 mysql:8.0
flask --app wsgi db upgrade -d database/migrations
python -m database.seed
flask --app wsgi run --debug
```

**Front end** (pasta `frontend`, Node.js):

```powershell
npm install
npm run dev
```

### Variáveis de ambiente (execução manual, arquivo `backend/.env`)

| Variável | Exemplo | Descrição |
|---|---|---|
| DB_HOST | localhost | Host do MySQL |
| DB_PORT | 3306 | Porta |
| DB_NAME | nassau_tickets | Banco |
| DB_USER | nassau | Usuário |
| DB_PASSWORD | nassau123 | Senha |
| JWT_SECRET | (texto longo aleatório) | Chave dos tokens |
| JWT_EXPIRE_MINUTES | 60 | Validade do token |
| EXPEDIENTE_LIVRE | false | `true` desliga a trava das 07h às 17h (somente demonstração) |

## Usuários de teste (criados pelo seed)

| Perfil | Login | Senha |
|---|---|---|
| GESTOR | gestor@nassau.com.br | Gestor@123 |
| ATENDENTE | usuario1@nassau.com.br ... usuario10@nassau.com.br | Atend@123 |

O seed também cria 10 guichês (1 a 10).

## Testes

```powershell
cd backend
python -m pytest -v
```

38 testes (máquina de estados, emissão, alternância, ciclo de atendimento, painel, TM, login, relatórios e administração). Usam SQLite em memória e não precisam do Docker.

Simulação de concorrência (exige MySQL no ar, seed aplicado e API parada; apaga as senhas do banco local):

```powershell
python -m tests.simular_concorrencia
```

Resultado obtido: 30 chamadas simultâneas por 10 atendentes, 30 senhas únicas, 0 duplicadas.

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
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React + Vite (Dockerfile e nginx.conf)
├── docs/                   # requisitos, diagramas e decisões
├── docker-compose.yml      # sobe banco, API e front
└── README.md
```

## API (resumo)

Tudo sob `/api/v1`. Documentação completa no Swagger.

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| GET | /health | público | Verifica API e banco |
| POST | /auth/login | público | Login, devolve JWT |
| POST | /senhas | público (totem) | Emite senha `{"tipo":"SP\|SG\|SE"}` |
| GET | /painel | público | 5 últimas senhas chamadas |
| POST | /atendimentos/chamar-proximo | ATENDENTE | Chama a próxima `{"guiche_id":1}` |
| POST | /atendimentos/{id}/chamar-novamente | ATENDENTE | Segunda chamada |
| POST | /atendimentos/{id}/iniciar | ATENDENTE | Inicia o atendimento |
| POST | /atendimentos/{id}/encerrar | ATENDENTE | Encerra o atendimento |
| POST | /atendimentos/{id}/nao-compareceu | ATENDENTE | Marca não comparecimento |
| GET | /relatorios/resumo, /detalhado, /tm, /auditoria, /indicadores | GESTOR | Aceitam `?data=AAAA-MM-DD` ou `?mes=AAAA-MM` |
| POST | /admin/descartar-sobras | GESTOR | Descarta senhas que sobraram |
| POST | /admin/usuarios | GESTOR | Cadastra usuário |

Rotas protegidas exigem `Authorization: Bearer <token>`. Erros seguem o formato `{"codigo": 403, "mensagem": "..."}`.

## Regras de negócio implementadas

* Senhas SP, SG e SE emitidas sem login, numeração `YYMMDD-PPSQ` com sequencial por tipo e reinício diário.
* Alternância `[SP] -> [SE|SG] -> [SP] -> [SE|SG]`, com SE antes de SG e tratamento de filas vazias.
* Qualquer guichê atende qualquer tipo de senha.
* Expediente das 07h às 17h (America/Recife) na emissão e na chamada.
* Máquina de estados com 7 estados (EMITIDA, AGUARDANDO, CHAMADA, CHAMADA_NOVAMENTE, EM_ATENDIMENTO, ATENDIDA, NAO_COMPARECEU), transições validadas e histórico em `senha_historico`.
* Duas chamadas sem comparecimento levam a NAO_COMPARECEU.
* Atendente com atendimento em andamento não chama outra senha.
* Descarte das sobras sem criar oitavo estado (campos `descartada_em` e `motivo_descarte`).
* TM simulado: SP 15 min (±5), SG 5 min (±3), SE 1 min (95%) ou 5 min (5%).
* Painel com as 5 últimas chamadas (nunca a próxima) e flag `ultima_chamada` para o áudio.
* Relatórios diário e mensal, auditoria e indicadores (espera média, não comparecimento, descarte, atendimentos por guichê e por atendente).

## Concorrência

Estratégia em três camadas na chamada da próxima senha:

1. `SELECT ... FOR UPDATE` na linha única de `estado_fila`: serializa a decisão (a alternância depende do estado anterior).
2. `FOR UPDATE SKIP LOCKED` na busca da senha.
3. `UNIQUE(senha_id)` em `atendimentos_auditoria`: o banco impede duas atribuições da mesma senha.

Evidência: `python -m tests.simular_concorrencia` (30 chamadas, 30 únicas, 0 duplicadas).

## Segurança e LGPD

* Senhas com hash argon2; autenticação JWT; controle de acesso por perfil.
* Cliente anônimo: nenhum dado pessoal é coletado, apenas a senha.
* Minimização e finalidade: guarda-se só o necessário para operação e auditoria.
* Registro de acesso em `log_acesso` (tentativas de login, sem gravar a senha).
* Mensagem de login genérica, sem revelar se o usuário existe.
* Segredos fora do código no uso manual (`.env` não versionado).

## Disponibilidade e falhas

* `GET /health` retorna 503 com mensagem padronizada quando o banco está indisponível.
* O pool de conexões usa `pool_pre_ping` para descartar conexões quebradas.
* Comportamento esperado do front/painel com a API ou o banco fora: manter a última tela, exibir "Sistema temporariamente indisponível" e tentar novamente a cada poucos segundos.
* Backup: `docker compose exec db mysqldump -unassau -pnassau123 nassau_tickets > backup.sql`.

## Integração com o front end

* Base da API: `http://localhost:5000/api/v1`; CORS liberado para `localhost` nas portas 5173, 4200 e 3000.
* Fluxo: login, guardar o token, enviar `Authorization: Bearer <token>`, chamar `chamar-proximo` e usar o `id` devolvido nos demais endpoints.
* O painel consulta `GET /painel` periodicamente; `ultima_chamada: true` indica tocar "Última chamada".
* Integração real validada: o totem emite senhas pela API (ex.: `261125-SP001`).

## Funcionalidades

**Implementadas:** tudo listado em "Regras de negócio implementadas", mais login, relatórios, cadastro de usuários, documentação OpenAPI e execução completa via Docker Compose.

**Não implementadas / limitações:**

* Descarte automático dos ~5% de senhas não atendidas: existe o serviço (`descarte_service`), mas sem agendamento automático.
* Descarte de fim de expediente acionado pelo gestor (`POST /admin/descartar-sobras`), sem agendador.
* Sequencial limitado a 999 senhas por tipo por dia (formato `SQ` com 3 dígitos).
* Sem recuperação de senha de usuário.
* O servidor Flask do compose é o de desenvolvimento, adequado à demonstração.

## Decisões de arquitetura

Camadas separadas (routers, services, repositories, models); `estado_fila` como ponto de bloqueio da concorrência; descarte sem oitavo estado; histórico de transições em tabela própria. Detalhes em `docs/`.

## Uso de IA generativa

Foi utilizada IA generativa (Claude, da Anthropic, e outra ferramenta de IA) como apoio na geração e revisão de código e documentação. A equipe revisou o material e é capaz de explicar o código produzido.