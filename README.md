# Helpdesk MCP

Sistema de demonstracao local para consultar chamados ficticios, ver o historico dos clientes e atualizar status. O projeto inclui um servidor MCP em Python/FastMCP, persistencia SQLite, especificacoes SDD e um cliente web Streamlit que se comunica com o servidor por `stdio`. Nao usa dados reais nem LLM.

## Estrutura

```text
helpdesk-mcp/
|-- app.py                         # Cliente web Streamlit
|-- helpdesk_chat.py               # Interpretador de comandos fixos em portugues
|-- helpdesk_mcp.py                # Servidor FastMCP, tools e inicializacao SQLite
|-- requirements.txt
|-- .vscode/mcp.json               # Registro MCP local no VS Code
|-- specs/
|   |-- missao.md                  # Constituicao: missao e limites
|   |-- pilha-tecnologia.md        # Constituicao: decisoes tecnicas
|   |-- roadmap.md                 # Fases e replanejamentos
|   |-- 01-listar-chamados/        # Requisitos, plano e validacao da Fase 1
|   |-- 02-historico-cliente/      # SDD e conclusao da Fase 2
|   `-- 03-atualizar-status/       # SDD e conclusao da Fase 3
`-- tests/                         # Testes das tools e comandos do chat
```

O banco `helpdesk.db` e criado automaticamente por `initialize_database()` na inicializacao do servidor. O esquema inclui clientes, chamados e eventos de historico; registros ficticios sao inseridos quando a tabela de chamados esta vazia. O banco e ignorado pelo Git para que cada ambiente mantenha seus dados locais.

## Instalacao

Requisito: Python 3.10 ou superior.

Linux/macOS:

```bash
cd helpdesk-mcp
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
cd helpdesk-mcp
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Cliente Streamlit

Na raiz do projeto e com o ambiente virtual ativo:

```bash
python -m streamlit run app.py
```

Abra o endereco local mostrado pelo Streamlit, normalmente `http://localhost:8501`. O cliente inicia o servidor MCP via `stdio` a cada comando e conserva a conversa em `st.session_state`.

Comandos suportados:

| Comando no chat | Tool chamada |
| --- | --- |
| `listar chamados` | `listar_chamados()` |
| `listar abertos` ou `quais chamados estao abertos?` | `listar_chamados(status="aberto")` |
| `historico cliente cli-001` | `buscar_historico_cliente(cliente_id="cli-001")` |
| `alterar chamado 3 para fechado` | `atualizar_status(chamado_id="HD-1003", novo_status="fechado")` |

IDs numericos de `1` a `3` correspondem a `HD-1001` a `HD-1003`. Tambem e possivel usar o ID completo. Status permitidos: `aberto`, `em_andamento`, `resolvido` e `fechado`. Comandos nao reconhecidos, status invalidos e IDs inexistentes recebem uma resposta de erro no chat.

## Servidor MCP no VS Code

Abra esta pasta como workspace. `.vscode/mcp.json` registra o servidor `helpdesk` com transporte `stdio` usando `.venv/bin/python` e `helpdesk_mcp.py`. Inicie/reinicie o servidor na vista MCP; as tools publicadas sao:

- `listar_chamados(status=None)` lista todos ou filtra por status.
- `buscar_historico_cliente(cliente_id)` retorna cliente, chamados e eventos cronologicos.
- `atualizar_status(chamado_id, novo_status, observacao=...)` persiste a transicao e acrescenta um evento sem apagar os anteriores.

Para escolher outro local do SQLite, defina `HELPDESK_DB_PATH` antes de iniciar. Para iniciar somente o servidor no terminal:

```bash
python helpdesk_mcp.py
```

O processo fica aguardando o cliente MCP em `stdio`; execute o Streamlit em outro terminal para conversar com ele.

## Validacao

Execute os testes automatizados:

```bash
python -m unittest discover -s tests -v
```

Os testes cobrem listagem e filtro, historico de cliente, atualizacoes, status invalido, chamado inexistente, preservacao do historico e rollback quando a escrita do evento falha. Tambem cobrem o mapeamento de comandos fixos do cliente.

Fluxo demonstrado no Streamlit:

1. `listar chamados` exibiu os tres registros.
2. `historico do cliente cli-001` exibiu Ana Souza, os dois chamados e os respectivos eventos.
3. `alterar chamado 3 para fechado` atualizou `HD-1003`; `liste fechados` confirmou o status persistido.
4. `alterar chamado 3 para pendente` foi rejeitado pelo servidor; uma frase fora dos comandos suportados mostrou instrucoes de uso.
5. `listar abertos` retornou lista vazia porque, no banco local usado para a demonstracao, o unico chamado aberto ja havia sido atualizado em execucoes anteriores. Em um banco recem-criado, o seed inicia `HD-1001` como `aberto`.