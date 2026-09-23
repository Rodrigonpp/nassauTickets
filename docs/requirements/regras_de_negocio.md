# Regras de Negócio do Sistema nassauTickets

## 1. Funcionamento e Expediente
* **RN-001 (Horário de Atendimento):** O expediente do laboratório ocorre estritamente das 07h00min às 17h00min. O sistema não deve permitir a chamada de novas senhas fora desse intervalo.
* **RN-002 (Encerramento do Expediente):** Atendimentos iniciados antes das 17h00min devem ser obrigatoriamente concluídos e encerrados pelo atendente através do sistema. Todas as senhas que permanecerem na fila após as 17h00min devem ser sumariamente descartadas.

## 2. Emissão e Formatação de Senhas
* **RN-003 (Identificação Anonimizada):** O cliente deve interagir de forma totalmente anônima com o totem para a geração de sua senha de atendimento.
* **RN-004 (Máscara Identificadora):** Toda senha emitida deve gerar uma numeração única que obedeça ao formato padrão YYMMDD-PPSQ, onde:
    * YY representa os dois dígitos finais do ano corrente;
    * MM representa os dois dígitos do mês corrente;
    * DD representa os dois dígitos do dia corrente;
    * PP representa o código de duas letras referente ao tipo da senha;
    * SQ representa o sequencial numérico de três dígitos por prioridade, com reinício diário obrigatório para 001.

## 3. Algoritmo de Priorização e Intercalação
* **RN-005 (Algoritmo de Atendimento Estrito):** A chamada de senhas pelo sistema deve intercalar obrigatoriamente as filas de acordo com o modelo de alternância [SP] -> [SE|SG] -> [SP] -> [SE|SG].
* **RN-006 (Atendimento Operacional Especial):** A Senha para Retirada de Exames (SE) possui curtíssimo tempo de atendimento e deve ser chamada no próximo guichê disponível sempre imediatamente após o encerramento do atendimento de uma Senha Prioritária (SP).
* **RN-007 (Tratamento de Filas Vazias):** Caso alguma das filas de priorização esteja temporariamente vazia durante o fluxo de intercalação, o sistema deve direcionar o atendimento para a próxima fila disponível seguindo a ordem de prioridades padrão (SP > SE > SG).
* **RN-008 (Polivalência de Guichês):** Não existem guichês dedicados a tipos específicos de senhas. Qualquer guichê disponível pode receber e processar qualquer um dos três tipos de senhas existentes (SP, SG ou SE).

## 4. Fluxo e Ciclo de Vida do Atendimento
* **RN-009 (Tentativas de Chamada e Abandono):** O atendente deve efetuar a primeira chamada da senha no painel. Caso o cliente não compareça ao guichê, o atendente pode acionar o comando de rechamada uma segunda vez. Se após duas chamadas consecutivas o cliente não se apresentar, o sistema deve alterar o estado da senha para "NÃO_COMPARECEU", considerá-la abandonada e passar para o próximo atendimento da fila.
* **RN-010 (Simulação Histórica de Desistência):** Para fins de simulação e consolidação dos relatórios gerenciais, o sistema deve considerar que aproximadamente 5% de todas as senhas de atendimento emitidas no Totem serão abandonadas por responsabilidade do cliente, devendo ser descartadas sem a execução do serviço de atendimento.
* **RN-011 (Ocultação de Próxima Senha):** O painel central de chamadas nunca deve calcular ou exibir de forma antecipada qual será a próxima senha da sequência. Novas senhas podem ser impressas no totem entre a finalização de um atendimento e o acionamento do painel pelo atendente, o que mudaria instantaneamente a ordem da fila.

## 5. Auditoria e Rastreabilidade
* **RN-012 (Campos em Branco para Não Atendidos):** No relatório detalhado de senhas, todos os campos referentes a horários de atendimento e guichê responsável devem permanecer obrigatoriamente em branco caso o cliente tenha abandonado a fila e a senha possua o status final "NÃO_COMPARECEU".
