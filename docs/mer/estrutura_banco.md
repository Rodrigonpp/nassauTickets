# Estrutura do Banco de Dados

## 1. Tabela: USUARIOS
Armazena os dados das pessoas que trabalham no laboratório.
* **id:** Número de identificação interno gerado automaticamente.
* **nome:** Nome completo do funcionário.
* **matricula:** Código de registro do funcionário, único para cada usuário.
* **login:** Nome de usuário para autenticação no sistema.
* **senha:** Senha criptografada.
* **perfil:** Define o nível de acesso da pessoa como ATENDENTE ou GESTOR.
* **ativo:** Indica se o funcionário está ativo no sistema (Verdadeiro ou Falso).

## 2. Tabela: GUICHES
Armazena a identificação dos locais físicos de atendimento.
* **id:** Número de identificação interno.
* **numero_guiche:** O número físico visível para o cliente (ex: Guichê 1, Guichê 2).
* **status:** Estado operacional atual do guichê (DISPONIVEL, OCUPADO ou INATIVO).

## 3. Tabela: SENHAS
Armazena de forma anônima os dados básicos das senhas geradas no Totem pelo Agente Cliente (AC).
* **id:** Número de identificação interno.
* **numero_senha:** O texto formatado exibido para o cliente (ex: 260923-SP001).
* **tipo_senha:** Categoria da senha (SP para Prioritária, SG para Geral, SE para Exames).
* **sequencial_diario:** O número sequencial isolado usado para controle de reinício diário automático.
* **status_atual:** Estado da senha no fluxo de atendimento (EMITIDA, AGUARDANDO, CHAMADA, CHAMADA_NOVAMENTE, EM_ATENDIMENTO, ATENDIDA, NAO_COMPARECEU).
* **data_hora_emissao:** O momento exato em que a senha foi gerada no Totem.

## 4. Tabela: ATENDIMENTOS_AUDITORIA
Associa as senhas aos atendentes e guichês correspondentes, registrando todos os marcos temporais exigidos para relatórios e auditoria.
* **id:** Número de identificação interno.
* **senha_id:** Identificador da senha tratada, vinculado à tabela de senhas.
* **usuario_id:** Identificador do atendente responsável, vinculado à tabela de usuários. Fica em branco se a senha não for chamada.
* **guiche_id:** Identificador do guichê onde ocorreu a chamada, vinculado à tabela de guichês. Fica em branco se a senha não for chamada.
* **horario_primeira_chamada:** Registro de data e hora do primeiro chamado no painel.
* **horario_segunda_chamada:** Registro de data e hora do segundo chamado (rechamada), se houver.
* **horario_inicio_atendimento:** Registro de data e hora em que o atendimento foi iniciado no guichê.
* **horario_finalizacao_atendimento:** Registro de data e hora de encerramento do atendimento.
