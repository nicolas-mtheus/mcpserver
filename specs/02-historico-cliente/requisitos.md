# Requisitos: historico do cliente

## Objetivo

Permitir que um agente MCP consulte os dados de um cliente e o historico dos chamados associados a ele.

## Requisitos funcionais

- **RF-01:** Disponibilizar a ferramenta MCP `buscar_historico_cliente(cliente_id)`.
- **RF-02:** Para um identificador existente, retornar os dados do cliente.
- **RF-03:** Retornar todos os chamados do cliente, incluindo identificador, assunto, descricao, status e datas.
- **RF-04:** Retornar os eventos de historico dos chamados do cliente, com chamado, status anterior e novo, observacao e data.
- **RF-05:** Ordenar os eventos cronologicamente, mantendo ordem deterministica para eventos com a mesma data.
- **RF-06:** Para cliente conhecido sem chamados, retornar listas vazias para chamados e historico.
- **RF-07:** Para identificador inexistente, rejeitar a consulta com mensagem clara.
- **RF-08:** Isolar o resultado ao cliente solicitado, sem incluir chamados ou eventos de outros clientes.

## Requisitos tecnicos

- Consultar SQLite com parametros, sem interpolar o identificador na SQL.
- Preservar a tool `listar_chamados` e o transporte MCP `stdio` existentes.
- Reutilizar o esquema `clients`, `tickets` e `ticket_history`, sem migracao.

## Criterios de aceite

1. `cli-001` retorna seus dois chamados e tres eventos de historico.
2. O historico de `cli-001` contem apenas eventos dos chamados desse cliente.
3. `cli-003`, cliente conhecido sem chamados, retorna listas vazias.
4. Um identificador desconhecido gera erro claro.
5. As tools anteriores continuam registradas e seus testes permanecem aprovados.