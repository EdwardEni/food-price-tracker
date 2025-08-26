import requests
from bs4 import BeautifulSoup
import csv
import logging

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
        products.append({
            "name": name.text.strip() if name else "",
            "price": price.text.strip() if price else "N/A",
        })
    return products

def save_to_csv(products, filename="products.csv"):
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
        save_to_csv(products)
    else:
        logging.error("No HTML content to parse")

if __name__ == "__main__":
    main()
