import os
import re
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sanitize(name):
    """Sanitize the search key to create a valid directory name."""
    return re.sub(r'[^\w\-_\.]', '_', name)

def scrape_search_key(search_key, file_path, search_url_template, num_images, headless, min_resolution, max_resolution, max_missed):
    """Scrape images for a single search key."""
    # Create subdirectory for the search key
    sub_dir = os.path.join(file_path, sanitize(search_key))
    os.makedirs(sub_dir, exist_ok=True)
    
    # Set up WebDriver
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Format search URL and navigate
    search_url = search_url_template.format(search_key=search_key)
    driver.get(search_url)
    logging.info(f"Scraping for '{search_key}' at {search_url}")
    
    # Initialize counters and storage
    saved = 0
    missed = 0
    counter = 1
    max_scrolls = 20
    seen_urls = set()
    
    for scroll in range(max_scrolls):
        # Scroll down to load more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load
        
        # Parse page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img_tags = soup.find_all('img')
        
        # Extract new image URLs
        new_urls = set()
        for img in img_tags:
            for attr in ['src', 'data-src', 'data-original']:
                if attr in img.attrs:
                    url = urljoin(driver.current_url, img[attr])
                    if url not in seen_urls:
                        new_urls.add(url)
                    break
        
        # Break if no new URLs are found
        if not new_urls:
            logging.info(f"No more new images found for '{search_key}' after {scroll + 1} scrolls")
            break
        
        # Process each new URL
        for url in new_urls:
            if saved >= num_images:
                break
            seen_urls.add(url)
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200 and response.headers['Content-Type'].startswith('image/'):
                    image = Image.open(BytesIO(response.content))
                    width, height = image.size
                    if (min_resolution[0] <= width <= max_resolution[0] and
                        min_resolution[1] <= height <= max_resolution[1]):
                        # Determine file extension
                        content_type = response.headers['Content-Type']
                        ext = '.jpg' if content_type == 'image/jpeg' else '.png' if content_type == 'image/png' else '.jpg'
                        filename = f"{sanitize(search_key)}_{counter:03d}{ext}"
                        file_path_full = os.path.join(sub_dir, filename)
                        image.save(file_path_full)
                        logging.info(f"Saved {file_path_full}")
                        saved += 1
                        counter += 1
                        missed = 0
                    else:
                        missed += 1
                        logging.debug(f"Image at {url} skipped due to resolution {width}x{height}")
                else:
                    missed += 1
                    logging.debug(f"Image at {url} skipped due to invalid response")
            except Exception as e:
                logging.error(f"Error processing {url}: {e}")
                missed += 1
            
            if missed >= max_missed:
                logging.info(f"Stopping '{search_key}' due to {max_missed} consecutive failures")
                break
        
        if saved >= num_images or missed >= max_missed:
            break
    
    driver.quit()
    logging.info(f"Finished scraping for '{search_key}', saved {saved} images")

def main(file_path, search_url_template, search_keys, number_of_images, headless, min_resolution, max_resolution, max_missed, number_of_workers):
    """Main function to scrape images for multiple search keys using parallel processing."""
    logging.info("Starting image scraping process")
    with ThreadPoolExecutor(max_workers=number_of_workers) as executor:
        futures = [
            executor.submit(
                scrape_search_key, key, file_path, search_url_template, number_of_images,
                headless, min_resolution, max_resolution, max_missed
            ) for key in search_keys
        ]
        for future in futures:
            future.result()  # Wait for all tasks to complete and handle exceptions
    logging.info("Image scraping process completed")

# Example usage
if __name__ == "__main__":
    # Define file path and website
    file_path = "./scraped_images"
    search_url_template = "https://www.google.com/search?tbm=isch&q={search_key}"  # Example for Google Images
    
    # Define search keys (add new keys here as needed)
    search_keys = ["brick", "bricks", "brick wall", "brick texture", "red brick"]
    
    # Define parameters
    number_of_images = 100
    headless = True
    min_resolution = (100, 100)  # Minimum width, height
    max_resolution = (1000, 1000)  # Maximum width, height
    max_missed = 10
    number_of_workers = 2
    
    # Run the program
    main(file_path, search_url_template, search_keys, number_of_images, headless, min_resolution, max_resolution, max_missed, number_of_workers)