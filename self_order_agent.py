"""Compatibility shim exposing `root_agent` for different import styles.

Some tools or entry points may look for a top-level module named
`self_order_agent` (underscored) or `self-order-agent` (dash). This file
re-exports `root_agent` from `agent.py` so imports like
`from self_order_agent import root_agent` work.
"""

try:
    from .agent import root_agent  # type: ignore
except Exception:
    # Fallback to direct import when executed as a script
    try:
        from agent import root_agent  # type: ignore
    except Exception:
        root_agent = None

__all__ = ["root_agent"]
