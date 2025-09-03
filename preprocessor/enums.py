from .mappings import *
from .utils import _series_from_enum, _normalize_key

class SoftwareType(Enum):
    Web = 1
    Desktop = 2
    Mobile = 3
    Hybrid = 4

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes)


class IndustryDomain(Enum):
    Ecommerce = 1
    Travel = 2
    Hotel_Management = 3
    Restaurant_Management = 4
    Content_Management = 5
    Social_Networking = 6
    Edtech = 7
    Healthcare = 8
    Fintech = 9
    Portfolio = 10
    Others = 11

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)


class TargetMarket(Enum):
    Local = 1
    Global = 2
    Both = 3

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)


class AdminDashboard(Enum):
    Null = 0
    Basic = 1
    Advanced = 2
    Professional = 3

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)


class ContentManagement(Enum):
    Null = 0
    Workflow = 1
    Pages_and_Media = 2
    Blog = 3

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)


class ExtraFeatures(Enum):
    Null = 0
    Search_and_Filter = 1
    AI_ML_Module = 2
    Reporting_and_Analysis = 3
    File_Handling = 4
    Offile_Mode = 5
    Data_Backup = 6
    Notification = 7

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)


class ThirdPartyService(Enum):
    Null = 0
    Analytics = 1
    Payment_Gateway = 2
    Map = 3
    Mail = 4

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        # Note: this enum is used for single-value fallback; if you have multi-values in a cell
        # you may prefer MultiLabelBinarizer downstream. This returns the first match.
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)


class Authentication(Enum):
    Null = 0
    Basic = 1
    Social = 2
    Multi_Factor = 3
    Biometric = 4

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)


class DataMigration(Enum):
    Null = 0
    No = 1
    Yes = 2

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)


class UIUXDesign(Enum):
    Basic = 1
    Advanced = 2
    Custom = 3

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)


class Performance(Enum):
    Basic = 1
    Medium = 2
    High = 3

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)


class Security(Enum):
    Null = 0
    Standard = 1
    High = 2

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)


class Availability(Enum):
    Normal = 1
    Always = 2

    @classmethod
    def from_series(cls, col: pd.Series, codes: bool = False, fallback: Optional[Any] = None) -> pd.Series:
        return _series_from_enum(cls, col, codes=codes, fallback=fallback)

