# utils.py
import pandas as pd
import numpy as np
from typing import Any, Optional

def _normalize_key(x: str) -> str:
    s = str(x).strip().lower()
    if s in ("null", "none", "nan", ""):
        return ""
    return "".join(ch for ch in s if ch.isalnum())

def _series_from_enum(cls: type, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
    """
    Generic converter: returns a pd.Series of Enum members (or ints if codes=True).
    """
    lookup = {}
    for name, member in cls.__members__.items():
        key = _normalize_key(name)
        if key:
            lookup[key] = member

    if fallback is None:
        if "Null" in cls.__members__:
            fallback_member = cls.__members__["Null"]
        elif "Others" in cls.__members__:
            fallback_member = cls.__members__["Others"]
        else:
            fallback_member = np.nan
    else:
        if isinstance(fallback, str):
            fallback_member = cls.__members__.get(fallback, np.nan)
        elif isinstance(fallback, cls):
            fallback_member = fallback
        else:
            fallback_member = np.nan

    def map_value(v):
        if pd.isna(v):
            return fallback_member
        if isinstance(v, (list, tuple, set)):
            for item in v:
                mapped = map_value(item)
                if not (isinstance(mapped, float) and np.isnan(mapped)):
                    return mapped
            return fallback_member
        s = str(v)
        key = _normalize_key(s)
        if not key:
            return fallback_member
        if key in lookup:
            return lookup[key]
        alt = s.strip().replace(" ", "_").replace("-", "_")
        alt_key = _normalize_key(alt)
        if alt_key in lookup:
            return lookup[alt_key]
        return fallback_member

    result = col.apply(map_value)

    if codes:
        return result.apply(lambda m: (m.value if isinstance(m, cls) else np.nan))
    else:
        return result
