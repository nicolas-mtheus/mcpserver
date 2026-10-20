"""Streamlit chat client for the local Helpdesk MCP server."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

import streamlit as st
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from helpdesk_chat import format_tool_result, parse_command


PROJECT_DIR = Path(__file__).resolve().parent
PYTHON = Path(os.environ.get("HELPDESK_PYTHON", PROJECT_DIR / ".venv" / "bin" / "python"))
SERVER_SCRIPT = PROJECT_DIR / "helpdesk_mcp.py"

st.set_page_config(
    page_title="Helpdesk | Atendimento local",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root {
        --ink: #182b2a;
        --muted: #6b7b76;
        --paper: #f3f5ef;
        --panel: #ffffff;
        --line: #dce4dc;
        --teal: #176b61;
        --lime: #c9e66b;
        --coral: #d66c4d;
    }
    html, body, [class*="css"] { font-family: 'Manrope', sans-serif; color: var(--ink); }
    .stApp { background: var(--paper); }
    [data-testid="stSidebar"] { background: #e7ede5; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] > div { padding-top: 1.4rem; }
    .brand-mark { font-family: 'DM Mono', monospace; color: var(--teal); font-size: .78rem; letter-spacing: .12em; text-transform: uppercase; }
    h1 { font-weight: 800 !important; letter-spacing: 0 !important; color: var(--ink); }
    .subhead { color: var(--muted); margin-top: -.55rem; }
    .status-line { display: flex; gap: .55rem; align-items: center; color: var(--muted); font-size: .82rem; margin: 1.2rem 0; }
    .status-dot { width: 9px; height: 9px; border-radius: 50%; background: var(--teal); box-shadow: 0 0 0 4px #176b6119; }
    .command-label { font-family: 'DM Mono', monospace; font-size: .7rem; text-transform: uppercase; color: var(--muted); letter-spacing: .08em; }
    code { font-family: 'DM Mono', monospace !important; color: var(--teal) !important; }
    [data-testid="stCode"] pre { white-space: pre-wrap !important; overflow-wrap: anywhere; }
    [data-testid="stChatMessage"] { border: 1px solid var(--line); border-radius: 8px; background: var(--panel); padding: 1rem 1.15rem; }
    [data-testid="stChatInput"] { border-color: #b9c9bf; }
    [data-testid="stChatInput"] textarea { font-family: 'Manrope', sans-serif; }
    .stButton button { border-radius: 6px; border-color: #cad7cc; color: var(--teal); font-weight: 700; }
    .stButton button:hover { border-color: var(--teal); color: var(--teal); background: #e8f0e7; }
    </style>
    """,
    unsafe_allow_html=True,
)


def _run_tool(tool_name: str, arguments: dict[str, Any]) -> Any:
    transport = StdioTransport(
        command=str(PYTHON),
        args=[str(SERVER_SCRIPT)],
        cwd=str(PROJECT_DIR),
    )

    async def invoke() -> Any:
        async with Client(transport) as client:
            result = await client.call_tool(tool_name, arguments)
            return result.structured_content

    return asyncio.run(invoke())


def _handle_command(text: str) -> dict[str, Any]:
    parsed = parse_command(text)
    if parsed is None:
        return {
            "role": "assistant",
            "content": (
                "Não reconheci esse comando. Tente `listar abertos`, "
                "`historico cliente cli-001` ou "
                "`alterar chamado 3 para fechado`."
            ),
        }

    tool_name, arguments = parsed
    try:
        result = _run_tool(tool_name, arguments)
        return {
            "role": "assistant",
            "content": format_tool_result(tool_name, result),
            "tool": tool_name,
            "data": result,
        }
    except Exception as error:
        return {
            "role": "assistant",
            "content": f"Não foi possível concluir a operação: {error}",
            "tool": tool_name,
        }


with st.sidebar:
    st.markdown('<div class="brand-mark">Helpdesk · MCP</div>', unsafe_allow_html=True)
    st.markdown('<div class="status-line"><span class="status-dot"></span>Servidor local · stdio</div>', unsafe_allow_html=True)
    st.markdown("### Comandos rápidos")
    st.markdown('<div class="command-label">Chamados</div>', unsafe_allow_html=True)
    st.code("listar abertos\nlistar chamados", language="text")
    st.markdown('<div class="command-label">Histórico</div>', unsafe_allow_html=True)
    st.code("historico cliente cli-001", language="text")
    st.markdown('<div class="command-label">Atualização</div>', unsafe_allow_html=True)
    st.code("alterar chamado 3\npara fechado", language="text")
    st.caption("IDs numéricos 1–3 apontam para HD-1001–HD-1003.")
    if st.button("Limpar conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div class="brand-mark">Atendimento local · dados fictícios</div>', unsafe_allow_html=True)
st.title("Central de chamados")
st.markdown('<p class="subhead">Consulte clientes, acompanhe ocorrências e atualize status pelo servidor MCP.</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá. Posso listar chamados, consultar o histórico de um cliente ou atualizar o status de um chamado. Use um dos comandos da lateral.",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("data") is not None:
            with st.expander("Ver dados retornados"):
                st.json(message["data"])

if prompt := st.chat_input("Ex.: listar abertos"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    response = _handle_command(prompt)
    st.session_state.messages.append(response)
    with st.chat_message("assistant"):
        st.markdown(response["content"])
        if response.get("data") is not None:
            with st.expander("Ver dados retornados"):
                st.json(response["data"])