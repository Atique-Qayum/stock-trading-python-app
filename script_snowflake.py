import requests
import os
import time
import snowflake.connector
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

LIMIT = 1000
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
REQUEST_DELAY = 12  # seconds between requests

# --- Snowflake Connection Details from .env ---
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_TABLE = os.getenv("SNOWFLAKE_TABLE")

def fetch_tickers():
    """Fetch all tickers from Polygon API with pagination and rate limiting"""
    url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"
    
    all_tickers = []
    page_count = 0
    
    try:
        while url:
            page_count += 1
            print(f"Fetching page {page_count}...")

            response = requests.get(url)

            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                continue

            response.raise_for_status()
            data = response.json()

            if "results" in data:
                all_tickers.extend(data["results"])
                print(f"Added {len(data['results'])} tickers (total: {len(all_tickers)})")

            # Pagination
            url = data.get('next_url')
            if url:
                url += f"&apiKey={POLYGON_API_KEY}"
                print(f"Next URL: {url}")
                time.sleep(REQUEST_DELAY)

    except requests.exceptions.RequestException as e:
        print(f"HTTP request failed: {e}")
        return None
    except ValueError as e:
        print(f"JSON parsing failed: {e}")
        return None
    except KeyboardInterrupt:
        print("Operation cancelled by user")
        return all_tickers
    
    return all_tickers

def write_tickers_to_snowflake(tickers):
    """Insert tickers into Snowflake table"""
    if not tickers:
        print("No tickers to insert")
        return False
    
    fieldnames = list(tickers[0].keys())  # dynamic columns
    
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
        cur = conn.cursor()

        # Create table if not exists (store all as STRING for simplicity)
        create_stmt = f"""
        CREATE TABLE IF NOT EXISTS {SNOWFLAKE_SCHEMA}.{SNOWFLAKE_TABLE} (
            {', '.join([f'{col.upper()} STRING' for col in fieldnames])}
        );
        """
        cur.execute(create_stmt)

        # Insert data
        placeholders = ",".join(["%s"] * len(fieldnames))
        insert_stmt = f"""
        INSERT INTO {SNOWFLAKE_SCHEMA}.{SNOWFLAKE_TABLE} ({",".join([col.upper() for col in fieldnames])})
        VALUES ({placeholders})
        """
        rows = []
        for ticker in tickers:
            row = [str(ticker.get(col, "")) for col in fieldnames]
            rows.append(row)
        
        cur.executemany(insert_stmt, rows)
        conn.commit()

        print(f"✅ Successfully inserted {len(rows)} rows into Snowflake table {SNOWFLAKE_SCHEMA}.{SNOWFLAKE_TABLE}")

        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f"⚠️ Snowflake insert error: {e}")
        return False

def main():
    print("🚀 Fetching tickers from Polygon API...")
    tickers = fetch_tickers()
    
    if tickers:
        print(f"📊 Retrieved {len(tickers)} tickers total")
        success = write_tickers_to_snowflake(tickers)
        if success:
            print("✅ Snowflake insert completed successfully")
        else:
            print("⚠️ Snowflake insert completed with errors")
    else:
        print("❌ Failed to fetch tickers")

if __name__ == "__main__":
    main()
