# Helpdesk MCP

Servidor MCP local de demonstracao para consultar e atualizar chamados ficticios. Consulte a constituicao do projeto em `specs/`.

## Preparar e executar

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python helpdesk_mcp.py
```

O servidor usa transporte `stdio`. No VS Code, abra esta pasta como workspace; `.vscode/mcp.json` configura o servidor `helpdesk` usando o ambiente virtual local.

O banco `helpdesk.db` e criado automaticamente ao iniciar. Para usar outro caminho, defina `HELPDESK_DB_PATH` antes de iniciar o servidor.

## Ferramentas

- `listar_chamados(status=None)`: lista chamados, opcionalmente filtrados por `aberto`, `em_andamento`, `resolvido` ou `fechado`.
- `buscar_historico_cliente(cliente_id)`: retorna o cliente, seus chamados e eventos de historico.
- `atualizar_status(chamado_id, novo_status, observacao=...)`: atualiza o status e registra o evento de historico.

## Testes

```bash
python -m unittest discover -s tests -v
```