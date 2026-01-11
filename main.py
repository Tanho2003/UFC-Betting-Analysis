import pandas as pd
import numpy as np

# --- STEP 1: LOAD DATA ---
try:
    df = pd.read_csv('ufc-master.csv')
    print("Data loaded successfully!")
except FileNotFoundError:
    print("Error: Could not find 'ufc-master.csv'.")

# --- STEP 2: SELECT & RENAME COLUMNS ---
# We select the "Moneyball" columns + the new "Prop Bet" columns
cols_to_keep = [
    'Date', 'RedFighter', 'BlueFighter', 
    'RedOdds', 'BlueOdds', 'Winner', 
    'WeightClass', 'TitleBout', 'Finish', 'Gender',
    'RKOOdds', 'BKOOdds', 'RSubOdds', 'BSubOdds' # Added these for advanced analysis
]

# Check if columns exist (safety check)
existing_cols = [c for c in cols_to_keep if c in df.columns]
df = df[existing_cols]

# --- STEP 3: CONVERT ODDS (The Math) ---
def get_decimal_odds(american_odds):
    if pd.isna(american_odds):
        return 0
    if american_odds > 0:
        return 1 + (american_odds / 100)
    else:
        return 1 + (100 / abs(american_odds))

# Convert Moneyline Odds
df['R_decimal'] = df['RedOdds'].apply(get_decimal_odds)
df['B_decimal'] = df['BlueOdds'].apply(get_decimal_odds)

# --- STEP 4: CALCULATE PROFIT (ROI Analysis) ---
# Simulate $100 bet on the Winner

# 4a. Red Profit
conditions_red = [
    (df['Winner'] == 'Red'),
    (df['Winner'] == 'Blue'),
    (df['Winner'] == 'Draw')
]
values_red = [
    (100 * (df['R_decimal'] - 1)), -100, 0
]
df['Red_Profit_100'] = np.select(conditions_red, values_red)

# 4b. Blue Profit
conditions_blue = [
    (df['Winner'] == 'Blue'),
    (df['Winner'] == 'Red'),
    (df['Winner'] == 'Draw')
]
values_blue = [
    (100 * (df['B_decimal'] - 1)), 
    -100, 
    0
]
df['Blue_Profit_100'] = np.select(conditions_blue, values_blue)

# --- STEP 5: FAVORITE vs UNDERDOG LOGIC ---
# Who was the favorite?
df['Favorite_Profit'] = np.where(df['RedOdds'] < df['BlueOdds'], df['Red_Profit_100'], df['Blue_Profit_100'])
df['Underdog_Profit'] = np.where(df['RedOdds'] > df['BlueOdds'], df['Red_Profit_100'], df['Blue_Profit_100'])

# --- STEP 6: CLEANUP & EXPORT ---
# Fix Date
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# Simplify "Finish" column for charts (Group "S-DEC", "U-DEC", "M-DEC" into "Decision")
def clean_finish(finish):
    if pd.isna(finish): return 'Unknown'
    if 'DEC' in finish: return 'Decision'
    if 'KO' in finish: return 'KO/TKO'
    if 'SUB' in finish: return 'Submission'
    return 'Other'

df['Method_Simplified'] = df['Finish'].apply(clean_finish)

# Rounding
cols_to_round = ['Red_Profit_100', 'Blue_Profit_100', 'Favorite_Profit', 'Underdog_Profit']
df[cols_to_round] = df[cols_to_round].round(2)

# Save
df.to_csv('UFC_Master_Cleaned.csv', index=False)
print("Transformation Complete! File 'UFC_Master_Cleaned.csv' created.")