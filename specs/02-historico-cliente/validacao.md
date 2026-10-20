# Validacao: historico do cliente

## Testes automatizados

Executar na raiz do projeto:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Casos cobertos:

- Cliente com chamados retorna os chamados e eventos esperados.
- Eventos sao ordenados deterministicamente e pertencem somente aos chamados do cliente.
- Cliente conhecido sem chamados retorna listas vazias.
- Cliente inexistente e rejeitado com mensagem clara.
- Regressao: listagem de chamados, filtro, atualizacao de status e validacoes anteriores.

## Validacao MCP local

1. A configuracao `.vscode/mcp.json` registra o servidor `helpdesk` por `stdio`.
2. No cliente MCP local, listar as ferramentas e invocar `buscar_historico_cliente` com `cliente_id="cli-001"`.
3. Confirmar dois chamados e tres eventos no resultado; a ferramenta `listar_chamados` deve continuar registrada.

## Resultados observados

- [x] Os 8 testes da suite passaram.
- [x] Cliente `cli-001` retorna dois chamados e tres eventos; a ordenacao dos eventos e deterministica e nao inclui eventos de outro cliente.
- [x] Cliente `cli-003` retorna `chamados=[]` e `historico=[]`.
- [x] Cliente inexistente e rejeitado; o teste existente verifica a mensagem `nao encontrado`.
- [ ] A pergunta foi executada manualmente no Copilot Chat do VS Code. A chamada via cliente MCP local valida o protocolo e a ferramenta, mas nao substitui esse teste manual da interface.