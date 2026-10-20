"""Parse fixed Portuguese commands for the Streamlit Helpdesk client."""

from __future__ import annotations

import re
import unicodedata
from typing import Any


STATUSES = {"aberto", "em_andamento", "resolvido", "fechado"}


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text.casefold())
    without_accents = "".join(
        character for character in decomposed
        if not unicodedata.combining(character)
    )
    return re.sub(r"\s+", " ", without_accents).strip()


def _normalize_status(value: str) -> str:
    return _normalize(value).replace(" ", "_")


def _ticket_id(value: str) -> str:
    normalized = value.upper()
    if normalized.isdigit():
        number = int(normalized)
        return f"HD-{1000 + number}" if 1 <= number <= 3 else f"HD-{number:04d}"
    return normalized


def parse_command(text: str) -> tuple[str, dict[str, Any]] | None:
    """Map a supported fixed command to a FastMCP tool call."""
    command = _normalize(text)

    history_match = re.search(
        r"historico(?: do)? cliente\s+([a-z0-9_-]+)",
        command,
    )
    if history_match:
        return "buscar_historico_cliente", {"cliente_id": history_match.group(1)}

    update_match = re.search(
        r"(?:alterar|atualizar|mudar)\s+(?:o\s+)?chamado\s+([a-z0-9-]+)\s+"
        r"(?:para|pra)\s+([a-z_ ]+?)(?:\s+(?:observacao|porque)\s+(.+))?$",
        command,
    )
    if update_match:
        ticket_id, requested_status, note = update_match.groups()
        return "atualizar_status", {
            "chamado_id": _ticket_id(ticket_id),
            "novo_status": _normalize_status(requested_status),
            "observacao": note or "Status atualizado pelo cliente Streamlit.",
        }

    if re.search(r"\b(abertos?|em andamento|resolvidos?|fechados?)\b", command):
        status_match = re.search(
            r"\b(abertos?|em andamento|resolvidos?|fechados?)\b", command
        )
        if status_match:
            status = _normalize_status(status_match.group(1))
            if status.endswith("s") and status not in STATUSES:
                status = status[:-1]
            return "listar_chamados", {"status": status}

    if re.search(r"\b(listar|liste|mostre|quais|todos|todas)\b", command):
        return "listar_chamados", {}

    return None


def format_tool_result(tool_name: str, result: Any) -> str:
    """Create a readable short response while retaining the full result in state."""
    if tool_name == "listar_chamados":
        tickets = result.get("result", result) if isinstance(result, dict) else result
        if not tickets:
            return "Nenhum chamado encontrado para esse filtro."
        lines = [
            f"**{ticket['id']} · {ticket['subject']}** — {ticket['status']}\n\n"
            f"Cliente: {ticket.get('client_name', ticket['client_id'])}"
            for ticket in tickets
        ]
        return "\n\n".join(lines)

    if tool_name == "buscar_historico_cliente":
        client = result["cliente"]
        tickets = result["chamados"]
        events = result["historico"]
        lines = [f"**{client['name']}** · `{client['id']}` · {client['email']}"]
        lines.append(f"Chamados: {len(tickets)} · eventos: {len(events)}")
        for ticket in tickets:
            lines.append(f"- **{ticket['id']} · {ticket['subject']}** — {ticket['status']}")
        return "\n".join(lines)

    if tool_name == "atualizar_status":
        if result.get("alterado"):
            return (
                f"Chamado **{result['chamado_id']}** atualizado: "
                f"{result['status_anterior']} → **{result['status_atual']}**."
            )
        return f"O chamado **{result['chamado_id']}** já estava com status `{result['status_atual']}`. Nenhuma alteração foi feita."

    return str(result)