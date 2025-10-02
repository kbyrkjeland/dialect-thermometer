"""Dialect definitions bundled per locale."""

from __future__ import annotations

from .hardanger import DIALECT as HARDANGER
from .sortland import DIALECT as SORTLAND

DIALECTS = {
    "hardanger": HARDANGER,
    "sortland": SORTLAND,
}

__all__ = ["DIALECTS"]
