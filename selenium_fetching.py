from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_rendered_html(url, wait_time=3):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # run without opening browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    driver.get(url)
    time.sleep(wait_time)  # allow JS to load
    
    html = driver.page_source
    driver.quit()
    
    return html

fetch_rendered_html(r"https://neurips.cc/virtual/2025/loc/san-diego/papers.html?filter=topic&search=Computer+Vision-%3EImage+and+Video+Generation&layout=detail")