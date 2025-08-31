import requests
from bs4 import BeautifulSoup
import csv
import logging
from datetime import datetime
import os

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status
        soup = BeautifulSoup(response.text, 'html.parser')

        # Adjust these selectors according to the actual website structure
        products = []
        product_elements = soup.select('.product-item')  # Example container selector
        for elem in product_elements:
            name_tag = elem.select_one('.product-name')
            price_tag = elem.select_one('.product-price')
            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True)
                products.append({'name': name, 'price': price, 'scraped_at': datetime.now().isoformat()})
        logging.info(f"Scraped {len(products)} products from {url}")
        return products

    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return []

def save_to_csv(data, filename='scraped_prices.csv'):
    fieldnames = ['name', 'price', 'scraped_at']
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csvfile.seek(0, 2)  # Go to the end of file
            if csvfile.tell() == 0:
                writer.writeheader()
            for row in data:
                writer.writerow(row)
        logging.info(f"Saved {len(data)} records to {filename}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    target_url = 'https://example.com/products'  # <-- Replace with actual URL
    scraped_data = scrape_page(target_url)
    if scraped_data:
        save_to_csv(scraped_data)
    else:
        logging.info("No data scraped.")
