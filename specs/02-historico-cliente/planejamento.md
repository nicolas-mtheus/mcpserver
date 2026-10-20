# Planejamento: historico do cliente

## Abordagem

1. Reutilizar o esquema SQLite validado no replanejamento: `clients`, `tickets` e `ticket_history`.
2. Consultar primeiro o cliente; responder com erro claro se nao existir.
3. Consultar chamados e eventos pelo relacionamento `tickets.client_id`, usando parametros SQL.
4. Ordenar os chamados de forma deterministica e os eventos por data e identificador do evento.
5. Expor o resultado pela ferramenta FastMCP `buscar_historico_cliente` sem remover `listar_chamados`.
6. Cobrir cliente com chamados, isolamento do cliente, cliente sem chamados e cliente inexistente.
7. Validar suite automatizada e invocacao da ferramenta via cliente MCP local `stdio`.

## Implementacao existente reutilizada

A ferramenta ja estava presente em `helpdesk_mcp.py` e registrada no servidor. O trabalho desta fase confirma o contrato por especificacao, amplia os testes de comportamento e registra a validacao, sem duplicar a implementacao nem alterar a tool anterior.

## Definicao de pronto

Todos os criterios de `requisitos.md` estao cobertos por testes ou invocacao MCP; a suite completa passa; `listar_chamados` continua disponivel; validacao e conclusao registram evidencias e eventuais verificacoes manuais pendentes.