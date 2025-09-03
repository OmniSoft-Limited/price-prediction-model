import re
from typing import Any, Optional
import numpy as np
import pandas as pd
from .enums import *  
from .mappings import *
from .utils import _series_from_enum, _normalize_key


class Preprocessor:
    """
    Preprocessor for your software-price dataset.
    Usage:
        pre = Preprocessor(df)          # or Preprocessor(None)
        pre.fit()
        df_trans = pre.transform()      # will use internal data
    Or:
        pre.transform(df)               # transform an external dataframe
    """

    __data: Optional[pd.DataFrame]

    def __init__(self, data: Optional[pd.DataFrame] = None):
        self.__data = data

    # --------------------
    # Helper functions
    # --------------------
    @staticmethod
    def numusers_midpoint(col: pd.Series) -> pd.Series:
        """Convert '10-50', '01-10', '30+' etc. to numeric midpoints / floats."""
        def _parse_value(v: Any) -> float:
            if pd.isna(v):
                return np.nan
            s = str(v).strip()
            if s.lower() in ("null", "none", "nan", ""):
                return np.nan
            s = s.replace(",", "").strip()
            # range: a-b
            if "-" in s:
                left, right = s.split("-", 1)
                la = re.search(r"(\d+)", left)
                ra = re.search(r"(\d+)", right)
                if la and ra:
                    a = int(la.group(1))
                    b = int(ra.group(1))
                    return (a + b) / 2.0
            # plus form: "30+"
            if s.endswith("+"):
                m = re.search(r"(\d+)", s)
                return float(m.group(1)) if m else np.nan
            # single number
            m = re.search(r"(\d+)", s)
            if m:
                return float(m.group(1))
            return np.nan

        return col.apply(_parse_value)

    @staticmethod
    def avg_enum_list_series(col: pd.Series, enum_cls: Optional[type] = None) -> pd.Series:
        """
        For list-like cells, compute the average numeric value:
          - If item is Enum -> use .value
          - If item is numeric -> use it
          - If item is string -> attempt enum_cls.from_series mapping (if provided) or match name
        Returns float series (np.nan if empty/unparseable).
        """
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
                    return [it.strip() for it in s.split(",") if it.strip()]
                return [s]
            return [cell]

        def _value_from_item(it: Any) -> Optional[float]:
            if pd.isna(it):
                return None
            # Enum instance
            if isinstance(it, Enum):
                return float(it.value)
            # numeric
            if isinstance(it, (int, float, np.integer, np.floating)):
                return float(it)
            s = str(it).strip()
            if s.lower() in ("null", "none", "nan", ""):
                return None
            # exact numeric string
            m = re.fullmatch(r"[-+]?\d+(\.\d+)?", s)
            if m:
                try:
                    return float(s)
                except:
                    pass
            # enum lookup by normalized name
            key = _norm(s)
            if enum_lookup and key in enum_lookup:
                return float(enum_lookup[key])
            # try mapping using enum_cls.from_series as last resort
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


    # --------------------
    # Field converters (return numeric series)
    # --------------------
    def _software_types(self, col: pd.Series) -> pd.Series:
        # returns integer codes (1..4) or np.nan
        return SoftwareType.from_series(col, codes=True)

    def _industry_domain(self, col: pd.Series) -> pd.Series:
        return IndustryDomain.from_series(col, codes=True)

    def _num_users(self, col: pd.Series) -> pd.Series:
        return Preprocessor.numusers_midpoint(col)

    def _target_market(self, col: pd.Series) -> pd.Series:
        return TargetMarket.from_series(col, codes=True)

    def _admin_dashboard(self, col: pd.Series) -> pd.Series:
        return AdminDashboard.from_series(col, codes=True)

    def _content_management(self, col: pd.Series) -> pd.Series:
        # average of enum values for list-cells
        return Preprocessor.avg_enum_list_series(col, enum_cls=ContentManagement)

    def _extra_features(self, col: pd.Series) -> pd.Series:
        return Preprocessor.avg_enum_list_series(col, enum_cls=ExtraFeatures)

    def _third_party_services(self, col: pd.Series) -> pd.Series:
        return Preprocessor.avg_enum_list_series(col, enum_cls=ThirdPartyService)

    def _authentication(self, col: pd.Series) -> pd.Series:
        return Authentication.from_series(col, codes=True)

    def _data_migration(self, col: pd.Series) -> pd.Series:
        return DataMigration.from_series(col, codes=True)

    def _ui_ux_design(self, col: pd.Series) -> pd.Series:
        return UIUXDesign.from_series(col, codes=True)

    def _performance(self, col: pd.Series) -> pd.Series:
        return Performance.from_series(col, codes=True)

    def _security(self, col: pd.Series) -> pd.Series:
        return Security.from_series(col, codes=True)

    def _availability(self, col: pd.Series) -> pd.Series:
        return Availability.from_series(col, codes=True)

    def transform(self, data: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Transform the DataFrame and return a new DataFrame with numeric features.
        If data is None, uses the DataFrame passed at initialization or via fit().
        """
        df = data if data is not None else self.__data
        if df is None:
            raise ValueError("No DataFrame provided to transform(). Pass data or initialize Preprocessor with data.")

        df = df.copy()

        # Map each column if present
        if "softwareType" in df.columns:
            df["softwareType"] = self._software_types(df["softwareType"])

        if "industryDomain" in df.columns:
            df["industryDomain"] = self._industry_domain(df["industryDomain"])

        if "numUsers" in df.columns:
            df["numUsers"] = self._num_users(df["numUsers"])

        if "targetMarket" in df.columns:
            df["targetMarket"] = self._target_market(df["targetMarket"])

        if "adminDashboard" in df.columns:
            df["adminDashboard"] = self._admin_dashboard(df["adminDashboard"])

        if "contentManagement" in df.columns:
            df["contentManagement"] = self._content_management(df["contentManagement"])
            
        if "extraFeatures" in df.columns:
            df["extraFeatures"] = self._extra_features(df["extraFeatures"])

        if "thirdPartyService" in df.columns:
            df["thirdPartyService"] = self._third_party_services(df["thirdPartyService"])

        if "authentication" in df.columns:
            df["authentication"] = self._authentication(df["authentication"])

        if "dataMigration" in df.columns:
            df["dataMigration"] = self._data_migration(df["dataMigration"])

        if "uiUxDesign" in df.columns:
            df["uiUxDesign"] = self._ui_ux_design(df["uiUxDesign"])

        if "performance" in df.columns:
            df["performance"] = self._performance(df["performance"])

        if "security" in df.columns:
            df["security"] = self._security(df["security"])

        if "availability" in df.columns:
            df["availability"] = self._availability(df["availability"])

        return df
