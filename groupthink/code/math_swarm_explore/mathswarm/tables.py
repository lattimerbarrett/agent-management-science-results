"""Small markdown tables with little fluff."""
from __future__ import annotations


def percent(value: float | None, digits: int = 0) -> str:
    return "" if value is None or value != value else f"{100 * value:.{digits}f}%"


def with_interval(stat: dict | None) -> str:
    """A summarized number as '41% (29-54)': the mean and its 95% interval."""
    if not stat or stat["mean"] != stat["mean"]:
        return ""
    return f"{percent(stat['mean'])} ({100 * stat['low']:.0f}-{100 * stat['high']:.0f})"


def markdown(header: list[str], rows: list[list]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return "\n".join(lines)
