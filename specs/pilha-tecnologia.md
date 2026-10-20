# Pilha tecnologica

## Decisoes obrigatorias

| Area | Decisao | Aplicacao |
| --- | --- | --- |
| Linguagem | Python | Implementacao do servidor e das operacoes de dados. |
| Biblioteca MCP | `fastmcp` | Registro e exposicao das ferramentas MCP. |
| Persistencia | SQLite | Banco local criado automaticamente, sem servico externo. |
| Transporte | `stdio` | Comunicacao local entre o cliente MCP e o processo do servidor. |

## Persistencia e inicializacao

- O modulo `sqlite3` da biblioteca padrao gerencia o banco.
- O arquivo `helpdesk.db` e criado junto ao servidor na primeira execucao; `HELPDESK_DB_PATH` pode definir outro caminho.
- A primeira inicializacao cria tabelas e registros demonstrativos de clientes, chamados e eventos de historico.
- Inicializacoes seguintes preservam os dados existentes e nao reaplicam os dados demonstrativos se ja houver chamados.

## Execucao

Instale as dependencias de `requirements.txt` no ambiente virtual do projeto e execute `python helpdesk_mcp.py`. O processo atende pelo transporte `stdio`; nao deve imprimir logs ou mensagens de diagnostico em `stdout`.