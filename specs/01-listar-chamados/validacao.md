# Validacao: listar chamados

## Testes automatizados

Executar a partir da raiz do projeto:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Casos relevantes:

- `test_database_is_seeded_and_status_filter_works`: seed e filtro por `aberto`.
- `test_invalid_status_is_rejected`: rejeicao de status desconhecido.

## Teste MCP local

1. Abrir a pasta `helpdesk-mcp` no VS Code. O arquivo `.vscode/mcp.json` registra o servidor `helpdesk` por `stdio`.
2. Iniciar ou reiniciar o servidor na vista MCP.
3. No Copilot Chat, perguntar: **"Quais chamados estao abertos?"**. A ferramenta deve retornar somente chamados com status `aberto`.
4. Perguntar: **"Liste todos os chamados"**. A ferramenta deve retornar a lista sem filtro.
5. Perguntar: **"Liste chamados com status pendente"**. A ferramenta deve informar que o status e invalido.

## Resultados observados na implementacao

- [x] A suite de testes passa: 7 testes aprovados.
- [x] O cliente MCP local conecta por `stdio`, anuncia as tres ferramentas e invoca `listar_chamados(status="aberto")`; a resposta contem somente `HD-1001`.
- [x] `.vscode/mcp.json` e JSON valido e registra o servidor local.
- [ ] As tres perguntas foram executadas manualmente no Copilot Chat do VS Code. Esse teste depende da interface do usuario e deve ser marcado apos a execucao manual.

## Resultado esperado para a consulta aberta

O seed inclui um chamado `HD-1001` com status `aberto`; a resposta deve conter esse chamado e nao incluir os chamados `HD-1002` ou `HD-1003`.