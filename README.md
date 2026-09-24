# nassauTickets

## Membros
| Nome | Matrícula | Papel |
|---------------|-----------|---------------|
| Rodrigo Nunes | 01777171 | Scrum Master |
| Ericlys Severino | 01656023 | Documentador |
| Othon Henrique | 01809897 | Desenvolvedor |
| Marcio José | 01813686 | Desenvolvedor |
| Daniel Dantas | 01254056 | Testador |

## Descrição
O **nassauTickets** é uma solução digital projetada para gerenciar o fluxo completo de atendimento ao usuário por meio de um sistema automatizado de tickets (chamados). A aplicação gerencia desde o momento em que o cliente emite uma senha de forma anônima em um totem de autoatendimento, passando pela triagem em fila com algoritmos estritos de intercalação e priorização, até a chamada no painel central e a consolidação dos dados em relatórios de auditoria e desempenho gerencial.

## Objetivo
Consolidar os conhecimentos práticos em engenharia de software e desenvolvimento web através da criação de um ecossistema integrado (Frontend, Backend e Banco de Dados). O sistema visa otimizar o tempo de espera no atendimento laboratorial, mitigar problemas clássicos de concorrência de chamadas simultâneas, e fornecer métricas precisas sobre a eficiência da operação de atendimento.

## Tecnologias utilizadas
**React 19** (JavaScript/JSX, Hooks, Context API)

## Informações sobre as branches
O repositório segue um modelo de fluxo de trabalho simplificado operando obrigatoriamente com duas ramificações principais de longa duração:
* **`main`**: Contém o código estável e a documentação do projeto.
* **`dev`**: Branch de desenvolvimento. Todos os commits de código, novas funcionalidades, correções, etc; serão colocadas nela para posterior validação e unificação na main (merge).

## Instruções para instalação e execução
### Pré-requisitos
* Node.js instalado
* Git instalado

### Instalação
1. Clonar o repositório na máquina local:
```bash
git clone https://github.com/Rodrigonpp/nassauTickets
cd nassauTickets
```

2. Instalar dependências
```bash
npm install
```

### Execução
1. Dentro do diretório, executar o comando para ativar um localhost:
```bash
npm run dev
```