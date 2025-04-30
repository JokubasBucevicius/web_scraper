import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from bs4 import BeautifulSoup
import tempfile
import os

os.system("pkill chrome || true")

def scrape_website(website):
    print("Launching Chrome Browser...")

    chrome_driver_path = "/usr/bin/chromedriver"
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"  # Or wherever Chrome installed in WSL
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # Optional, but recommended inside WSL
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-data-dir=/tmp/selenium-profile")
    # temp_profile = tempfile.mkdtemp()
    # options.add_argument(f"--user-data-dir={temp_profile}")


    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        driver.get(website)
        print("Page loaded...")
        html = driver.page_source
        time.sleep(random.uniform(10, 20))

        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=8000):
    return [
        dom_content[i: i+max_length] for i in range(0, len(dom_content), max_length)
    ]

def scrape_website_with_pages(website, max_pages = 5):
    print("Launching Chrome Browser...")

    chrome_driver_path = "./chromedriver"
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"  # Or wherever Chrome installed in WSL
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # Optional, but recommended inside WSL
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--user-data-dir=/tmp/selenium-profile")
    # temp_profile = tempfile.mkdtemp()
    # options.add_argument(f"--user-data-dir={temp_profile}")


    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")



    all_html_pages = []

    try:
        for page_number in range(1, max_pages + 1):
            paginated_url = website.replace("/1", f"/{page_number}")

            print(f"Visiting page {page_number}: {paginated_url}")
            driver.get(paginated_url)

            time.sleep(random.uniform(10, 20))

            # Check if we were silently redirected back to page 1
            current_url = driver.current_url
            expected_part = f"/{page_number}?"
            if expected_part not in current_url:
                print(f"Redirect detected (expected page {page_number}, got {current_url}). Stopping.")
                break
                
            all_html_pages.append(driver.page_source)

        return all_html_pages
    finally:
        driver.quit()



