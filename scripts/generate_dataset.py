import pandas as pd
import numpy as np
import random

# --- Configuration ---
NUM_SAMPLES = 20  # Generating 20 high-quality, diverse samples.

# --- Feature Definitions ---
# Using the specific feature set you provided.
# NOTE: Added a single quote ' before numUsers values to prevent Excel auto-formatting issues.
feature_options = {
    'projectName': [f'Project_{i+1}' for i in range(NUM_SAMPLES)],
    'softwareType': ['Web', 'Mobile', 'Desktop', 'Hybrid/Cloud'],
    'industryDomain': ['E-commerce', 'Education/EdTech', 'Healthcare', 'FinTech', 'Social Networking', 'Content Management', 'Restaurant Management', 'Hotel Management', 'Logistics', 'Travel', 'Other'],
    'numUsers': ["'1-5", "'6-10", "'11-50", "'50-100", "'100+"],
    'targetMarket': ['Local', 'Global', 'Both'],
    'targetPlatforms': ['iOS', 'Android', 'Web', 'Desktop', 'Tablet/Smart Devices'],
    'authentication': ['None', 'Basic login', 'Social login', 'Enterprise SSO', 'Multi-factor authentication'],
    'adminDashboard': ['None', 'Basic', 'Advanced', 'Professional'],
    'ecommerce': ['None', 'Product catalog', 'Cart & Checkout', 'Payment gateway', 'Shipping & Inventory'],
    'contentManagement': ['None', 'Blog/News', 'Pages & Media uploads', 'Workflow'],
    'communicationFeatures': ['None', 'Notifications', 'Messaging/Chat', 'Real-time updates'],
    'extraFeatures': ['None', 'Search & Filters', 'Reporting & Analytics', 'Offline mode', 'File/media handling', 'AI/ML module'],
    'thirdPartyServices': ['None', 'Payment gateways', 'Maps/GPS', 'Email/SMS', 'Analytics', 'Other'],
    'dataMigration': ['Yes', 'No'],
    'uiUxDesign': ['Simple', 'Custom', 'Advanced'],
    'accessibility': ['Yes', 'No'],
    'performance': ['Basic', 'Medium', 'High'],
    'securityCompliance': ['Standard', 'High-security', 'Regulatory compliance'],
    'availability': ['Normal', '24/7 uptime'],
    'timeline': ['Flexible', '1-3 months', '3-6 months', '6-12 months', 'Urgent'],
}

# --- Price Calculation Logic (in USD) ---
# Weights are adjusted based on 2025 market analysis for software development.
# Complex features now have a significantly higher impact on the final cost.
price_weights = {
    'softwareType': {'Web': 200, 'Mobile': 250, 'Desktop': 350, 'Hybrid/Cloud': 500},
    'numUsers': {"'1-5": 500, "'6-10": 1500, "'11-50": 4000, "'50-100": 8000, "'100+": 18000},
    'authentication': {'None': 0, 'Basic login': 1200, 'Social login': 2500, 'Enterprise SSO': 9000, 'Multi-factor authentication': 7500},
    'adminDashboard': {'None': 0, 'Basic': 3500, 'Advanced': 11000, 'Professional': 22000},
    'ecommerce': {'None': 0, 'Product catalog': 4500, 'Cart & Checkout': 6500, 'Payment gateway': 8500, 'Shipping & Inventory': 11500},
    'extraFeatures': {'None': 0, 'Search & Filters': 3000, 'Reporting & Analytics': 14000, 'Offline mode': 9000, 'File/media handling': 6000, 'AI/ML module': 45000},
    'uiUxDesign': {'Simple': 2500, 'Custom': 10000, 'Advanced': 25000},
    'accessibility': {'Yes': 7000, 'No': 0},
    'performance': {'Basic': 0, 'Medium': 9000, 'High': 28000},
    'securityCompliance': {'Standard': 5000, 'High-security': 20000, 'Regulatory compliance': 50000},
    'availability': {'Normal': 0, '24/7 uptime': 18000},
    'timeline': {'Flexible': -2000, '1-3 months': 12000, '3-6 months': 4000, '6-12 months': 0, 'Urgent': 25000},
}

def calculate_price(features):
    """Calculates a simulated project price in USD based on feature weights."""
    base_price = 150  # A base price for initial consultation.
    
    # Sum the weights of the selected features
    for feature, value in features.items():
        if feature in price_weights and value in price_weights[feature]:
            base_price += price_weights[feature][value]
            
    # Introduce some random noise to make the data less deterministic
    noise = np.random.normal(loc=1.0, scale=0.10) # Fluctuate price by +/- 10% for realism
    final_price = base_price * noise
    
    # Ensure price is not negative and round to the nearest dollar
    return round(max(1500, final_price))


# --- Data Generation ---
print(f"Generating {NUM_SAMPLES} synthetic data samples...")

# Initialize a dictionary to hold the generated data
dataset = {key: [] for key in feature_options.keys()}
dataset['price'] = [] # Add the target variable column (price in USD)

# Generate each sample row
for i in range(NUM_SAMPLES):
    current_features = {}
    for feature, options in feature_options.items():
        # For projectName, use the pre-defined list
        if feature == 'projectName':
            chosen_value = options[i]
        else:
            # For all other features, pick a random option
            chosen_value = random.choice(options)
        
        current_features[feature] = chosen_value
        dataset[feature].append(chosen_value)
    
    # Calculate the price for the current set of features
    price = calculate_price(current_features)
    # --- FIX: Use the string 'price' as the key ---
    dataset['price'].append(price)

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(dataset)

# --- Export to CSV ---
output_filename = 'software_price_prediction_dataset.csv'
df.to_csv(output_filename, index=False)

print("-" * 30)
print(f"Successfully generated dataset with {len(df)} rows.")
print(f"Data saved to '{output_filename}'")
print("\nFirst 5 rows of the dataset:")
print(df.head())
print("-" * 30)

