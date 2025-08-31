import requests
import logging
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

def download_file(url, save_path):
    try:
        logging.info(f"Downloading from: {url}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info(f"Saved file to: {save_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to download {url}: {e}")
        return False

if __name__ == "__main__":
    # Direct CSV download URL from the Global WFP Food Prices dataset on HDX
    csv_url = "https://data.humdata.org/dataset/4fdcd4dc-5c2f-43af-a1e4-93c9b6539a27/resource/12d7c8e3-eff9-4db0-93b7-726825c4fe9a/download/wfpvam_foodprices.csv"
    save_location = "data/raw/wfpvam_foodprices.csv"
    success = download_file(csv_url, save_location)
    if success:
        logging.info("CSV download completed successfully.")
    else:
        logging.error("CSV download failed.")
