import requests
from bs4 import BeautifulSoup
import csv
import logging
import os

logging.basicConfig(level=logging.INFO)

def fetch_page(url):
    headers = {"User-Agent": "food-price-bot/1.0 (+mailto:semekray@yahoo.com)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        logging.error(f"Failed to fetch page {url}: {e}")
        return None

def parse_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []

    for product in soup.select("article.c-prd"):
        name = product.select_one("h3.name")
        price = product.select_one("div.prc")
        price_text = price.text.strip() if price else "N/A"
        # Clean price text to numeric string (remove currency symbol and commas)
        price_number = price_text.replace('₦', '').replace(',', '').strip() if price_text != "N/A" else price_text
        products.append({
            "name": name.text.strip() if name else "",
            "price": price_number,
        })
    return products

def save_to_csv(products, filename="data/clean/food_prices_clean.csv"):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price"])
        writer.writeheader()
        writer.writerows(products)
    logging.info(f"Saved {len(products)} products to {filename}")

def main():
    url = "https://www.jumia.com.ng/groceries/"
    html = fetch_page(url)
    if html:
        products = parse_products(html)
        if products:
            save_to_csv(products)
        else:
            logging.warning("No products found on page")
    else:
        logging.error("No HTML content to parse")

if __name__ == "__main__":
    main()
