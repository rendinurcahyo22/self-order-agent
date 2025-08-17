"""Package exports for the self-order-agent project.

This module tries to export `root_agent` from `agent.py` in a way that
works when the package is imported normally and when files are executed
or tested directly (pytest imports modules by path).
"""

try:
	# If imported as a package (preferred)
	from .agent import root_agent  # type: ignore
except Exception:
	# Allow importing the module directly (e.g., `from agent import root_agent`)
	try:
		from agent import root_agent  # type: ignore
	except Exception:
		# If neither import works, provide a placeholder to avoid import errors
		root_agent = None

__all__ = ["root_agent"]
