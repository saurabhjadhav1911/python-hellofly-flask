from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def get_chrome_driver():
    """Initialize Chrome WebDriver with headless options for server."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Use chromium from system path (installed via apt in Dockerfile)
    service = Service("/usr/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=options)
    return driver

@app.route("/")
def hello():
    return "Hello from Fly.io with Selenium!"

@app.route("/scrape")
def scrape_example():
    """Example endpoint that uses Selenium to scrape a website."""
    try:
        driver = get_chrome_driver()
        
        # Example: Get page title
        driver.get("https://example.com")
        page_title = driver.title
        
        driver.quit()
        
        return jsonify({
            "status": "success",
            "page_title": page_title,
            "message": "Selenium scraping successful"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
