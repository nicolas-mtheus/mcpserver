# Roadmap

## Fase 1 - `listar_chamados`

**Concluida.** A ferramenta consulta todos os chamados ou filtra por status (`aberto`, `em_andamento`, `resolvido` ou `fechado`). A validacao automatizada cobre a listagem, o filtro e a rejeicao de status desconhecido; a chamada MCP local por `stdio` tambem confirmou o filtro `aberto`.

**Aceite atendido:** a ferramenta retorna os campos principais, lista sem filtro, filtra pelo status solicitado e rejeita status desconhecido com mensagem clara.

## Fase 2 - `buscar_historico_cliente`

**Concluida.** A ferramenta retorna os dados do cliente, seus chamados e eventos de historico em ordem cronologica, rejeita identificadores desconhecidos e retorna listas vazias para cliente conhecido sem chamados.

**Aceite atendido:** cliente conhecido retorna seus chamados e alteracoes de status; identificador inexistente produz erro claro; cliente sem chamados retorna listas vazias de chamados e historico. Os 8 testes automatizados passaram.

## Fase 3 - `atualizar_status`

**Concluida.** A ferramenta atualiza chamados existentes para status permitidos e acrescenta eventos de auditoria sem apagar o historico anterior. A operacao e atomica no SQLite.

**Aceite atendido:** status invalido e chamado inexistente sao rejeitados sem escrita; falha ao inserir evento reverte a alteracao do chamado; repetir o status atual nao altera dados nem cria evento. Os 10 testes automatizados passaram.

## Criterio transversal

O banco e os registros ficticios sao criados automaticamente na primeira execucao. As tres fases devem ser acessiveis por ferramentas MCP via transporte `stdio` e cobertas por testes locais sem depender de dados ou servicos externos.

## Reavaliacao do banco apos a Fase 1

**Decisao: o esquema atual atende as Fases 2 e 3; nao e necessaria uma migracao neste momento.**

- `clients` identifica cada cliente e fornece nome e e-mail para a consulta de historico.
- `tickets.client_id` relaciona cada chamado ao cliente, permitindo listar seus chamados e retornar uma lista vazia quando ele nao possui chamados.
- `ticket_history` guarda o chamado, status anterior e novo, observacao e data. Isso permite compor o historico do cliente e registrar alteracoes de status.
- As chaves estrangeiras protegem os relacionamentos; o `CHECK` em `tickets.status` restringe os valores permitidos no banco.
- A Fase 3 deve atualizar `tickets` e inserir o evento correspondente em `ticket_history` na mesma transacao, como ja previsto na implementacao.

Os registros iniciais de historico representam a abertura e as mudancas existentes. Se fases futuras precisarem auditar outros tipos de evento alem de status, o formato de `ticket_history` devera ser revisto nessa evolucao, sem bloquear o escopo atual.

## Replanejamento para atualizacao de status

- **Status:** reutilizar a lista fechada definida em `STATUSES` e pelo `CHECK` do SQLite. Valores fora dela devem ser rejeitados antes da escrita.
- **Chamado inexistente:** consultar pelo identificador antes de atualizar; se nao existir, retornar erro claro e nao criar evento de historico.
- **Preservacao do historico:** cada transicao real deve atualizar `tickets` e inserir um novo registro em `ticket_history` na mesma transacao. Eventos anteriores sao append-only para esta funcionalidade.
- **Mesmo status:** tratar como operacao sem mudanca, sem atualizar a data nem inserir evento duplicado.
- **Auditoria do evento:** registrar status anterior, novo status, observacao e data/hora UTC. Em caso de falha na escrita do evento, a atualizacao do chamado tambem deve sofrer rollback.

A Fase 2 (`buscar_historico_cliente`) permanece **concluida**. Sua consulta ordena eventos por data e identificador, e exibira os novos eventos acrescentados pela Fase 3 sem exigir alteracao do esquema.