# Roadmap

## Fase 1 - `listar_chamados`

**Concluida.** A ferramenta consulta todos os chamados ou filtra por status (`aberto`, `em_andamento`, `resolvido` ou `fechado`). A validacao automatizada cobre a listagem, o filtro e a rejeicao de status desconhecido; a chamada MCP local por `stdio` tambem confirmou o filtro `aberto`.

**Aceite atendido:** a ferramenta retorna os campos principais, lista sem filtro, filtra pelo status solicitado e rejeita status desconhecido com mensagem clara.

## Fase 2 - `buscar_historico_cliente`

**Concluida.** A ferramenta retorna os dados do cliente, seus chamados e eventos de historico em ordem cronologica, rejeita identificadores desconhecidos e retorna listas vazias para cliente conhecido sem chamados.

**Aceite atendido:** cliente conhecido retorna seus chamados e alteracoes de status; identificador inexistente produz erro claro; cliente sem chamados retorna listas vazias de chamados e historico. Os 8 testes automatizados passaram.

## Fase 3 - `atualizar_status`

Atualizar o status de um chamado existente e inserir um evento de historico com status anterior, novo status, data e observacao.

**Aceite:** a mudanca e persistida; status invalido ou chamado inexistente e rejeitado; repetir o status atual nao cria evento duplicado.

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