# Roadmap

## Fase 1 - `listar_chamados`

Implementar a consulta de todos os chamados, com filtro opcional por status (`aberto`, `em_andamento`, `resolvido` ou `fechado`).

**Aceite:** a ferramenta retorna os campos principais de cada chamado; sem filtro lista todos e com filtro retorna somente o status solicitado. Status desconhecido e rejeitado com mensagem clara.

## Fase 2 - `buscar_historico_cliente`

Consultar um cliente pelo identificador e retornar seus dados, chamados e eventos de historico em ordem cronologica.

**Aceite:** cliente conhecido retorna seus chamados e alteracoes de status; identificador inexistente produz erro claro; cliente sem chamados retorna uma lista vazia de chamados.

## Fase 3 - `atualizar_status`

Atualizar o status de um chamado existente e inserir um evento de historico com status anterior, novo status, data e observacao.

**Aceite:** a mudanca e persistida; status invalido ou chamado inexistente e rejeitado; repetir o status atual nao cria evento duplicado.

## Criterio transversal

O banco e os registros ficticios sao criados automaticamente na primeira execucao. As tres fases devem ser acessiveis por ferramentas MCP via transporte `stdio` e cobertas por testes locais sem depender de dados ou servicos externos.