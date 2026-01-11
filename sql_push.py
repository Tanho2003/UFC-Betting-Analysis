import pandas as pd
from sqlalchemy import create_engine

# 1. Load the data
df = pd.read_csv('UFC_Master_Cleaned.csv')

# 2. Connect to Postgres
db_string = "postgresql://postgres:Kendeptrai115$@localhost:5432/ufc_db"
db = create_engine(db_string)

# 3. Push the data
print("⏳ Importing data to SQL...")
df.to_sql('fact_ufc_betting', db, if_exists='replace', index=False)
print("✅ Success! Data is now in Postgres.")