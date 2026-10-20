# Requisitos: listar chamados

## Objetivo

Permitir que um agente MCP consulte os chamados ficticios armazenados localmente no Helpdesk MCP, com opcao de filtrar pelo status.

## Requisitos funcionais

- **RF-01:** Disponibilizar a ferramenta MCP `listar_chamados`.
- **RF-02:** Sem argumento de status, retornar todos os chamados existentes.
- **RF-03:** Com status, retornar apenas chamados daquele status.
- **RF-04:** Aceitar somente `aberto`, `em_andamento`, `resolvido` e `fechado` como status de filtro.
- **RF-05:** Retornar para cada chamado identificador, identificador e nome do cliente, assunto, descricao, status e datas de criacao e atualizacao.
- **RF-06:** Rejeitar status desconhecido com mensagem clara, sem executar consulta com filtro invalido.

## Requisitos de dados e operacao

- Usar SQLite local e a tabela de chamados relacionada a clientes.
- Criar o banco, esquema e registros ficticios automaticamente na primeira inicializacao.
- Permitir configurar o caminho do banco por `HELPDESK_DB_PATH`.
- Expor a ferramenta pelo servidor FastMCP com transporte `stdio`.
- Nao escrever saida de aplicacao em `stdout`, que e reservado ao protocolo MCP.

## Fora de escopo

- Dados reais, acesso remoto, autenticacao, autorizacao e interface web.
- Alteracao de chamados, coberta por fase posterior do roadmap.

## Criterios de aceite

1. A listagem sem filtro retorna os registros demonstrativos.
2. Um filtro valido retorna somente chamados com status correspondente.
3. Um filtro invalido gera erro claro.
4. A ferramenta aparece no cliente MCP local e pode ser invocada via `stdio`.