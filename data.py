import requests
import pandas as pd
import sqlite3

def fetch_and_store():
    url = "https://data.cityofchicago.org/resource/iqnk-2tcu.json?$limit=1000"
    response = requests.get(url)
    df = pd.DataFrame(response.json())
    conn = sqlite3.connect("health.db")
    df.to_sql("health", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Stored {len(df)} rows")
    return df

if __name__ == "__main__":
    df = fetch_and_store()
    print(df.columns.tolist())
    print(df.head())
