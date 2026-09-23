# Requisitos - nassauTickets

## 1. Requisitos Funcionais (RF)

### Módulo do Totem (Agente Cliente - AC)
* **RF-001:** Emitir senhas de atendimento anonimamente de forma física ou virtual.
* **RF-002:** Disponibilizar três opções de categorias para emissão da senha: Senha Prioritária (SP), Senha Geral (SG) e Senha para Retirada de Exames (SE).
* **RF-003:** Gerar a numeração automática da senha obedecendo ao formato padrão YYMMDD-PPSQ, onde SQ é a sequência por prioridade reiniciada diariamente.

### Módulo do Terminal (Agente Atendente - AA)
* **RF-004:** Chamar a próxima senha da fila respeitando o algoritmo de intercalação obrigatório [SP] -> [SE|SG] -> [SP] -> [SE|SG].
* **RF-005:** Chamar novamente a senha atual ativa no guichê.
* **RF-006:** Iniciar formalmente o atendimento assim que o cliente se apresentar ao guichê.
* **RF-007:** Finalizar o atendimento ativo, liberando o guichê para a próxima chamada.
* **RF-008:** Realizar login no sistema utilizando credenciais válidas.

### Módulo do Painel de Chamadas (Agente Sistema - AS)
* **RF-009:** Exibir de forma destacada a senha chamada da vez e o número do guichê correspondente.
* **RF-010:** Manter o histórico visual visível das 5 últimas senhas chamadas.
* **RF-011:** Ocultar qualquer previsão ou exibição da próxima senha antes que ocorra o acionamento oficial do atendente.
* **RF-012:** Emitir áudio por voz sintetizada durante a chamada informando a prioridade, o sequencial da senha e o guichê.
* **RF-013:** Adicionar a indicação falada "Última chamada" caso o atendente acione o comando de rechamada.

### Módulo do Gestor
* **RF-014:** Emitir relatórios quantitativos gerais e por prioridade, diários e mensais, das senhas emitidas e atendidas.
* **RF-015:** Emitir relatório detalhado com numeração, tipo, data e hora da emissão, data e hora do atendimento e guichê.
* **RF-016:** Emitir relatório de tempo médio de atendimento segregado por tipo de senha.
* **RF-017:** Emitir relatório de auditoria detalhado rastreando atendente, guichê, senha, horários de primeira e segunda chamadas, início e término do atendimento.

---

## 2. Requisitos Não Funcionais (RNF)

### Tecnologia e Arquitetura
* **RNF-001:** O Frontend da aplicação deve ser desenvolvido utilizando React.
* **RNF-002:** O Banco de Dados relacional utilizado deve ser o MySQL 8.0.
* **RNF-003:** O Backend deve ser estruturado em arquitetura de API REST utilizando Python 3.14.

### Concorrência e Desempenho
* **RNF-004:** O sistema deve gerenciar e tratar conflitos de concorrência caso dois ou mais atendentes solicitem a próxima senha simultaneamente, prevenindo a entrega da mesma senha para guichês diferentes.
* **RNF-005:** As transações de requisição de senhas devem possuir tempo de resposta baixo para evitar gargalos operacionais no Totem e nos terminais.

### Segurança, Conformidade e Legislação
* **RNF-006:** O sistema deve estar em conformidade com a LGPD, assegurando o anonimato dos pacientes na emissão de senhas e relatórios públicos.
* **RNF-007:** A interface do painel e do totem devem respeitar as diretrizes da Lei de Acessibilidade, garantindo contrastes adequados e leitura facilitada.
* **RNF-008:** Controle de perfis de acesso rígido onde apenas usuários autenticados com o perfil de Gestor possam acessar a geração de relatórios e cadastros.

### Disponibilidade e Resiliência
* **RNF-009:** Em cenários de falha no Backend ou no Banco de Dados, as interfaces do Frontend devem possuir mecanismos de tratamento para exibir mensagens de erro ou indisponibilidade sem quebrar o sistema.
