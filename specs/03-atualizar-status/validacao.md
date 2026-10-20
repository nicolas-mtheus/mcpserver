# Validacao: atualizar status

## Testes automatizados

Executar na raiz do projeto:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Casos especificos:

- Transicao valida persiste o novo status e acrescenta evento sem remover os anteriores.
- Status invalido nao altera o chamado nem o historico.
- Chamado inexistente e rejeitado sem inserir evento.
- Status repetido nao gera evento duplicado.
- Uma trigger SQLite que rejeita a insercao do evento comprova rollback da atualizacao do chamado.

## Cliente MCP

- O servidor deve anunciar `listar_chamados`, `buscar_historico_cliente` e `atualizar_status`.
- Invocar `atualizar_status` e depois `buscar_historico_cliente` deve revelar a transicao nova ao lado dos eventos anteriores.
- A configuracao local continua em `.vscode/mcp.json` e usa transporte `stdio`.

## Resultados observados

- [x] 10 testes automatizados aprovados.
- [x] O teste de falha forcada na escrita do historico confirmou rollback e nenhum estado parcial.
- [x] Cliente MCP `stdio` anunciou `listar_chamados`, `buscar_historico_cliente` e `atualizar_status`.
- [x] A chamada MCP atualizou `HD-1001` para `em_andamento`; `buscar_historico_cliente` retornou o novo evento e preservou os tres eventos anteriores.
- [ ] A interacao visual no Copilot Chat do VS Code ainda depende de execucao manual pelo usuario.