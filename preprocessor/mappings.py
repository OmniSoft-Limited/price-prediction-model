# mappings.py
import re
import numpy as np
import pandas as pd
from typing import Any, Optional
from .enums import *   # or `import enums` and use enums.SoftwareType, etc.
from enum import Enum

def numusers_midpoint(col: pd.Series) -> pd.Series:
    def _parse_value(v: Any) -> float:
        if pd.isna(v):
            return np.nan
        s = str(v).strip()
        if s.lower() in ("null", "none", "nan", ""):
            return np.nan
        s = s.replace(",", "").strip()
        if "-" in s:
            left, right = s.split("-", 1)
            la = re.search(r"(\d+)", left)
            ra = re.search(r"(\d+)", right)
            if la and ra:
                a = int(la.group(1))
                b = int(ra.group(1))
                return (a + b) / 2.0
        if s.endswith("+"):
            m = re.search(r"(\d+)", s)
            return float(m.group(1)) if m else np.nan
        m = re.search(r"(\d+)", s)
        if m:
            return float(m.group(1))
        return np.nan
    return col.apply(_parse_value)

def avg_enum_list_series(col: pd.Series, enum_cls: Optional[type] = None) -> pd.Series:
    def _norm(s: str) -> str:
        return "".join(ch for ch in str(s).strip().lower() if ch.isalnum())
    enum_lookup = {}
    if enum_cls is not None:
        for name, member in enum_cls.__members__.items():
            enum_lookup[_norm(name)] = member.value

    def _cell_to_list(cell: Any):
        if isinstance(cell, (list, tuple, set)):
            return list(cell)
        if isinstance(cell, str):
            s = cell.strip()
            if s.startswith("[") and s.endswith("]"):
                items = re.split(r",\s*", s[1:-1])
                items = [it.strip().strip("'\"") for it in items if it.strip().strip("'\"")]
                return items
            if "," in s:
                items = [it.strip() for it in s.split(",") if it.strip()]
                return items
            return [s]
        return [cell]

    def _value_from_item(it: Any) -> Optional[float]:
        if pd.isna(it):
            return None
        if isinstance(it, Enum):
            return float(it.value)
        if isinstance(it, (int, float, np.integer, np.floating)):
            return float(it)
        s = str(it).strip()
        if s.lower() in ("null", "none", "nan", ""):
            return None
        import re as _re
        m = _re.fullmatch(r"[-+]?\d+(\.\d+)?", s)
        if m:
            try:
                return float(s)
            except:
                pass
        key = _norm(s)
        if enum_lookup and key in enum_lookup:
            return float(enum_lookup[key])
        if enum_cls is not None:
            mapped = enum_cls.from_series(pd.Series([s]), codes=True).iloc[0]
            if not pd.isna(mapped):
                return float(mapped)
        return None

    def _avg_cell(cell: Any) -> float:
        items = _cell_to_list(cell)
        nums = []
        for it in items:
            v = _value_from_item(it)
            if v is not None and not (isinstance(v, float) and np.isnan(v)):
                nums.append(v)
        if not nums:
            return np.nan
        return float(np.mean(nums))

    return col.apply(_avg_cell)