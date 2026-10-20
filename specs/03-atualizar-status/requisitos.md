# Requisitos: atualizar status

## Objetivo

Permitir que um agente MCP altere o status de um chamado ficticio, preservando a auditoria de todas as transicoes reais.

## Requisitos funcionais

- **RF-01:** Disponibilizar a ferramenta MCP `atualizar_status(chamado_id, novo_status, observacao)`.
- **RF-02:** Aceitar somente `aberto`, `em_andamento`, `resolvido` e `fechado`.
- **RF-03:** Rejeitar status invalido com mensagem clara e sem alterar chamado ou historico.
- **RF-04:** Rejeitar chamado inexistente com mensagem clara e sem criar evento.
- **RF-05:** Em transicao real, persistir o novo status e `updated_at` no SQLite.
- **RF-06:** Acrescentar evento com status anterior, novo status, observacao e data/hora UTC, sem apagar eventos anteriores.
- **RF-07:** Atualizacao do chamado e insercao do evento devem ser atomicas; falha em qualquer escrita nao pode deixar estado parcial.
- **RF-08:** Se o chamado ja estiver no status solicitado, retornar `alterado=false`, sem atualizar `updated_at` nem inserir evento.

## Requisitos de compatibilidade

- Preservar `listar_chamados` e `buscar_historico_cliente`.
- Manter SQLite, FastMCP e transporte local `stdio`.
- Preservar o contrato de leitura do historico, que deve exibir eventos novos em ordem cronologica.

## Criterios de aceite

1. Status permitido atualiza o chamado e acrescenta exatamente um evento.
2. Status invalido e chamado inexistente sao rejeitados sem escrita.
3. Falha ao inserir evento reverte tambem a mudanca do status.
4. Transicao repetida nao duplica historico.
5. As tres ferramentas sao anunciadas pelo servidor MCP e as ferramentas anteriores seguem funcionando.