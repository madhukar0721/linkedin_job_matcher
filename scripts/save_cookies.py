
import pickle
from pathlib import Path
from selenium import webdriver
import time
COOKIES_PATH = Path("cookies/linkedin_cookies.pkl")

def save_linkedin_cookies():
    driver = webdriver.Chrome() 
    driver.get("https://www.linkedin.com/login")
    input("🔐 Log in to LinkedIn and press Enter once ready...")
    time.sleep(120)
    cookies = driver.get_cookies()
    COOKIES_PATH.parent.mkdir(exist_ok=True)
    with COOKIES_PATH.open("wb") as f:
        pickle.dump(cookies, f)
    print(f"✅ Cookies saved to {COOKIES_PATH}")
    driver.quit()

if __name__ == "__main__":
    save_linkedin_cookies()