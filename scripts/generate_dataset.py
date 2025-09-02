import random
import pandas as pd
from pathlib import Path

# Import your Enums
from data_struct import (
    SoftwareType,
    IndustryDomain,
    TargetMarket,
    AdminDashboard,
    ContentManagement,
    ExtraFeatures,
    ThirdPartyService,
    Authentication,
    DataMigration,
    UIUXDesign,
    Performance,
    Security,
    Availability
)

# Possible ranges
NUM_USERS_OPTIONS = ["1-10", "10-30", "30-50", "50-100", "100-500", "500-1000"]
TIMELINE_MONTHS = [3, 4, 6, 9, 12, 18, 24, 30, 36]

def random_enum_choice(enum_cls):
    """Pick a random member name from an Enum class (skip numeric value)."""
    return random.choice(list(enum_cls)).name

def generate_row():
    return {
        "softwareType": random_enum_choice(SoftwareType),
        "industryDomain": random_enum_choice(IndustryDomain),
        "numUsers": random.choice(NUM_USERS_OPTIONS),
        "targetMarket": random_enum_choice(TargetMarket),
        "adminDashboard": random_enum_choice(AdminDashboard),
        "contentManagement": random_enum_choice(ContentManagement),
        "extraFeatures": random_enum_choice(ExtraFeatures),
        "thirdPartyService": random_enum_choice(ThirdPartyService),
        "authentication": random_enum_choice(Authentication),
        "dataMigration": random_enum_choice(DataMigration),
        "uiUxDesign": random_enum_choice(UIUXDesign),
        "performance": random_enum_choice(Performance),
        "security": random_enum_choice(Security),
        "availability": random_enum_choice(Availability),
        "timeline_months": random.choice(TIMELINE_MONTHS),
        # price generated based on complexity factors (rough)
        "price": random.randint(40000, 200000)
    }

def main():
    rows = [generate_row() for _ in range(50)]
    df = pd.DataFrame(rows)

    out_path = Path("../dataset/data-struct.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"✅ Dataset saved to {out_path.resolve()}")

if __name__ == "__main__":
    main()
