# Missao do projeto

## Proposito

Disponibilizar um servidor MCP local para consultar e atualizar chamados de um sistema de helpdesk ficticio. O servidor oferece ferramentas pequenas e previsiveis para que um agente MCP possa apoiar o atendimento sem acessar um sistema externo.

## Usuarios

- **Agentes MCP:** assistentes e clientes compatíveis com MCP que invocam as ferramentas do servidor.
- **Agentes de suporte:** pessoas que consultam chamados, acompanham o historico dos clientes e atualizam status.

## Escopo

- Listar chamados, com filtro opcional por status.
- Consultar o historico de chamados de um cliente.
- Atualizar o status de um chamado e registrar a alteracao no historico.
- Criar automaticamente o banco SQLite e registros demonstrativos na primeira execucao.

## Limites

- Todos os dados sao ficticios e servem apenas para demonstracao e desenvolvimento.
- O servidor e executado localmente e usa transporte `stdio`.
- Nao ha autenticacao, autorizacao, acesso a rede, integracao com servicos reais ou garantia de uso em producao.
- O banco e armazenado localmente; remover o arquivo SQLite apaga os dados locais e permite recriar a demonstracao.