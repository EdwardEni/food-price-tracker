import pandas as pd
from sqlalchemy import create_engine, text
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Database config - update your credentials
DB_USER = "postgres"
DB_PASS = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "food_price_db"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Deduplication window in days
DEDUP_DAYS = 7

def clean_data(df):
    df['product_name'] = df['product_name'].str.strip()
    df['price'] = (
        df['price']
        .astype(str)
        .str.replace('₦', '')
        .str.replace(',', '')
        .str.strip()
    )
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])  # Drop rows where price conversion failed
    
    df['currency'] = df.get('currency', 'NGN')
    df['scrape_date'] = pd.to_datetime(df.get('scrape_date', datetime.now()), errors='coerce')
    df['product_url'] = df['product_url'].fillna('unknown').str.strip()
    df['source'] = df.get('source', 'Jumia')
    df['brand'] = df.get('brand', None)
    
    return df

def load_to_db(df):
    engine = create_engine(DATABASE_URL)
    with engine.begin() as conn:  # Transaction scope
        for _, row in df.iterrows():
            # Deduplicate by source + product_url + scrape_date within last DEDUP_DAYS
            query = text("""
                SELECT id FROM food_prices
                WHERE source = :source
                AND product_url = :product_url
                AND scrape_date >= (CURRENT_DATE - INTERVAL ':dedup_days day')
                LIMIT 1
            """)
            existing = conn.execute(query, {
                "source": row['source'],
                "product_url": row['product_url'],
                "dedup_days": DEDUP_DAYS
            }).fetchone()

            if existing:
                logging.info(f"Skipping duplicate: {row['product_name']} ({row['product_url']})")
                continue

            # Insert fresh record
            insert_query = text("""
                INSERT INTO food_prices (product_name, price, currency, product_url, brand, source, scrape_date)
                VALUES (:product_name, :price, :currency, :product_url, :brand, :source, :scrape_date)
            """)
            conn.execute(insert_query, {
                "product_name": row['product_name'],
                "price": row['price'],
                "currency": row['currency'],
                "product_url": row['product_url'],
                "brand": row['brand'],
                "source": row['source'],
                "scrape_date": row['scrape_date']
            })
            logging.info(f"Inserted: {row['product_name']}")

def main():
    raw_csv_path = 'data/raw/products.csv'  # Update CSV path as needed
    try:
        df = pd.read_csv(raw_csv_path)
        logging.info(f"Loaded {len(df)} records from raw CSV")

        df_clean = clean_data(df)
        load_to_db(df_clean)
        logging.info("ETL load completed successfully")

    except Exception as e:
        logging.error(f"ETL load failed: {e}")

if __name__ == "__main__":
    main()
