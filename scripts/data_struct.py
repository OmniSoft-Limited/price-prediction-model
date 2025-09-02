from enum import Enum

class SoftwareType(Enum):
    Web = 1
    Desktop = 2
    Mobile = 3
    Hybrid = 4

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

class TargetMarket(Enum):
    Local = 1
    Global = 2
    Both = 3

class AdminDashboard(Enum):
    Null = 0
    Basic = 1
    Advanced = 2
    Professional = 3

class ContentManagement(Enum):
    Null = 0
    Workflow = 1
    Pages_and_Media = 2
    Blog = 3

class ExtraFeatures(Enum):
    Null = 0
    Search_and_Filter = 1
    AI_ML_Module = 2
    Reporting_and_Analysis = 3
    File_Handling = 4
    Offile_Mode = 5
    Data_Backup = 6
    Notification = 7

class ThirdPartyService(Enum):
    Null = 0
    Analytics = 1
    Payment_Gateway = 2
    Map = 3
    Mail = 4

class Authentication(Enum):
    Null = 0
    Basic = 1
    Social = 2
    Multi_Factor = 3
    Biometric = 4

class DataMigration(Enum):
    Null = 0
    No = 1
    Yes = 2

class UIUXDesign(Enum):
    Basic = 1
    Advanced = 2
    Custom = 3

class Performance(Enum):
    Basic = 1
    Medium = 2
    High = 3

class Security(Enum):
    Null = 0
    Standard = 1
    High = 2

class Availability(Enum):
    Normal = 1
    Always = 2

