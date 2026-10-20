# Planejamento: listar chamados

## Abordagem

1. Reutilizar a inicializacao SQLite e os dados demonstrativos do servidor Helpdesk MCP.
2. Implementar a consulta com filtro parametrizado, validando o status contra o conjunto permitido.
3. Registrar `listar_chamados` como ferramenta FastMCP e manter o transporte `stdio`.
4. Cobrir listagem, filtro valido e status invalido com testes automatizados.
5. Validar a configuracao do VS Code e invocar a ferramenta por um cliente MCP local.

## Superficies existentes reutilizadas

- Servidor: `helpdesk_mcp.py`.
- Testes: `tests/test_helpdesk_mcp.py`.
- Registro local no VS Code: `.vscode/mcp.json`.
- Ambiente/dependencias: `.venv` e `requirements.txt`.

## Riscos e mitigacoes

- **Banco preexistente sem registros de demonstracao:** seed somente quando a tabela de chamados estiver vazia; testes usam banco temporario isolado.
- **Filtro SQL inseguro:** usar consulta parametrizada e lista fechada de status.
- **Protocolo contaminado por logs:** FastMCP controla a comunicacao e a aplicacao nao imprime em `stdout`.

## Definicao de pronto

Os criterios de aceite de `requisitos.md` estao cobertos pelos testes, o servidor anuncia a ferramenta via `stdio`, e os documentos de validacao registram comandos e resultados observados.