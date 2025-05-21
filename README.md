# Image Scraper

This Python-based image scraper uses Selenium and BeautifulSoup to extract images from websites based on search keys and customizable parameters. It’s designed for tasks like building datasets, content aggregation, or research, with features like headless browsing, resolution filtering, and parallel processing.

## Features
- Scrapes images from websites using search keys.
- Saves images into subdirectories named after search keys.
- Supports headless browsing for GUI-less operation.
- Filters images by minimum and maximum resolution.
- Handles errors gracefully with logging and a maximum failure threshold.
- Uses parallel threads to scrape multiple search keys efficiently.

## Prerequisites
Clone the repository or download the script:
```bash
git clone https://github.com/LeoCheung0804/image-scraper.git
cd image-scraper
```
or download the ZIP file and extract it.

To run this program, ensure you have Python installed (version 3.6 or higher recommended). You’ll also need to install the following libraries:

- `beautifulsoup4` - Parses HTML content.
- `selenium` - Automates browser interactions.
- `requests` - Downloads images.
- `Pillow` - Processes image files.
- `webdriver-manager` - Manages ChromeDriver automatically.

Install them using pip:
```bash
pip install -r requirements.txt
```

## Configuration
Edit the `main` function in `image_scraper.py` or create a configuration section with the following parameters:

- **File Path**: Directory to save images (e.g., `"./scraped_images"`).
- **Website URL Template**: URL with a placeholder for search keys (e.g., `"https://www.google.com/search?tbm=isch&q={search_key}"` for Google Images).
- **Search Keys**: List of search terms (e.g., `["cute cats", "beautiful landscapes"]`).
- **Parameters**:
  - `number_of_images`: Number of images to scrape per search key (e.g., `10`).
  - `headless`: Set to `True` for no browser GUI, `False` to see the browser (e.g., `True`).
  - `min_resolution`: Tuple of (width, height) for minimum image size (e.g., `(200, 200)`).
  - `max_resolution`: Tuple of (width, height) for maximum image size (e.g., `(1920, 1080)`).
  - `max_missed`: Max consecutive failed downloads before stopping (e.g., `5`).
  - `number_of_workers`: Number of parallel threads (e.g., `2`).

Example configuration in `image_scraper.py`:
```python
def main():
    file_path = "./scraped_images"
    search_url_template = "https://www.google.com/search?tbm=isch&q={search_key}"
    search_keys = ["cute cats", "beautiful landscapes"]
    params = {
        "number_of_images": 10,
        "headless": True,
        "min_resolution": (200, 200),
        "max_resolution": (1920, 1080),
        "max_missed": 5,
        "number_of_workers": 2
    }
    # Call scraping function here
```

## Usage
Run the script from your terminal:
```bash
python image_scraper.py
```

### What Happens When You Run It?
1. Subdirectories are created for each search key in the specified `file_path`.
2. Chrome launches (headless or visible) and navigates to the search URL for each key.
3. The script scrolls to load images, extracts URLs, and downloads images meeting resolution criteria.
4. Images are saved as files in their respective subdirectories.
5. Progress and errors are logged for troubleshooting.

## Ethical and Legal Considerations
- **Website Terms**: Check the target website’s terms of service and `robots.txt` file. Some sites, like Google, may restrict automated scraping.
- **Copyright**: Ensure you have permission to use downloaded images, as they may be copyrighted.
- **Rate Limiting**: The script includes a delay (e.g., `time.sleep(2)`) to avoid overloading servers. Adjust this if needed.

## Troubleshooting
- **No Images Downloaded**: Verify the URL template and website compatibility. Some sites may block automated access.
- **ChromeDriver Issues**: Ensure `webdriver-manager` installed correctly and your Chrome version is compatible.
- **Resolution Errors**: Check `min_resolution` and `max_resolution` values—images outside these bounds won’t download.

## Customization
- **Change Websites**: Modify the `search_url_template` and adjust the image extraction logic if the site’s structure differs.
- **Enhance Logging**: Increase logging verbosity in the script for detailed debugging.
- **Optimize Speed**: Adjust `number_of_workers` based on your system’s capacity.

## Dependencies
- Python 3.6+
- Libraries: `beautifulsoup4`, `selenium`, `requests`, `Pillow`, `webdriver-manager`

## Resources
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Web Scraping Best Practices](https://oxylabs.io/blog/web-scraping-best-practices)

## License
This project is provided as-is for educational purposes. Ensure compliance with legal and ethical guidelines when using it.

---

Happy scraping!