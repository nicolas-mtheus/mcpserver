# Planejamento: atualizar status

## Abordagem

1. Validar `novo_status` contra a lista fechada `STATUSES` antes de abrir a escrita.
2. Buscar o chamado pelo identificador parametrizado; retornar erro se ausente.
3. Se o status ja for o solicitado, retornar sem tocar no chamado nem no historico.
4. Para transicao real, atualizar `tickets` e inserir o evento de `ticket_history` dentro de uma unica transacao SQLite.
5. Manter os eventos existentes; somente acrescentar uma linha por transicao real.
6. Testar sucesso, persistencia, preservacao, status invalido, chamado inexistente, repeticao e rollback forçado da insercao do historico.
7. Validar a lista de tools e invocar as operacoes por cliente MCP local `stdio`.

## Implementacao reutilizada

`atualizar_status` ja existia em `helpdesk_mcp.py`, validava os status e executava as duas escritas sob o context manager da conexao SQLite. Esta fase confirma o comportamento com testes de falha transacional e regressao; nao altera o contrato publico da ferramenta.

## Definicao de pronto

Todos os criterios de `requisitos.md` passam, as tres ferramentas MCP continuam registradas, o roadmap marca a Fase 3 concluida e os commits da feature e da integracao ficam publicados.