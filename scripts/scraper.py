import pickle
import time
from typing import Any, Dict, List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scripts.config import (
    BASE_URL, COOKIES_PATH, COMPANIES_FILE, TITLES_FILE,
    GEO_ID_INDIA, EXPERIENCE_LEVELS, TIME_RANGE, FILTER_FUNCTIONAL
)
from scripts.utils import human_delay, clean_text_for_llm, load_json


def login_with_cookies() -> webdriver.Chrome:
    """
    Launch Chrome, restore LinkedIn session via cookies.
    """
    driver = webdriver.Chrome(service=Service())
    driver.get(BASE_URL)
    time.sleep(2)
    cookies = pickle.loads(COOKIES_PATH.read_bytes())
    for cookie in cookies:
        cookie.pop("sameSite", None)
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(5)
    return driver


def build_search_url(company_ids: List[str], title_codes: List[str]) -> str:
    """Construct LinkedIn job search URL with filters."""
    from urllib.parse import quote_plus
    params = {
        "f_C": ",".join(company_ids),
        "geoId": GEO_ID_INDIA,
        "f_TPR": TIME_RANGE,
        "f_E": ",".join(map(str, EXPERIENCE_LEVELS)),
        "f_F": ",".join(FILTER_FUNCTIONAL),
        "f_T": ",".join(title_codes),
    }
    query = "&".join(f"{k}={quote_plus(v)}" for k, v in params.items())
    return f"{BASE_URL}/jobs/search/?{query}"


def extract_job_cards(driver: webdriver.Chrome) -> List[Any]:
    """Wait for and return job cards."""
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-view-name="job-card"]')))
    return driver.find_elements(By.CSS_SELECTOR, '[data-view-name="job-card"]')


def scroll_to_load_all(driver: webdriver.Chrome, pause: float = 0.5) -> None:
    """Scroll until no new cards appear."""
    while True:
        cards = extract_job_cards(driver)
        if not cards:
            return
        before = len(cards)
        driver.execute_script("arguments[0].scrollIntoView(true);", cards[-1])
        time.sleep(pause)
        after = len(extract_job_cards(driver))
        if after == before:
            return


def scrape_all_jobs() -> List[Dict[str, Any]]:
    """Log in, paginate, and scrape all matching job postings."""
    companies = load_json(COMPANIES_FILE)
    titles = load_json(TITLES_FILE)
    company_ids = [c["id"] for c in companies]
    valid_names = [c["name"] for c in companies]
    title_codes = [t["code"] for t in titles]

    url = build_search_url(company_ids, title_codes)
    driver = login_with_cookies()
    results: List[Dict[str, Any]] = []
    try:
        driver.get(url)
        human_delay()
        while True:
            scroll_to_load_all(driver)
            cards = extract_job_cards(driver)
            print(f"[+] Found {len(cards)} cards on this page")
            for card in cards:
                try:
                    company = card.find_element(By.CSS_SELECTOR, 'div.artdeco-entity-lockup__subtitle span').text
                    if company not in valid_names:
                        continue
                    title = card.find_element(By.CSS_SELECTOR, 'a.job-card-list__title--link').text
                    location = card.find_element(By.CSS_SELECTOR, 'ul.job-card-container__metadata-wrapper li').text
                    link = card.find_element(By.CSS_SELECTOR, 'a.job-card-list__title--link').get_attribute("href")

                    card.click()
                    human_delay()
                    desc = driver.find_element(By.ID, "job-details").text
                    description = clean_text_for_llm(desc)
                    results.append({
                        "Company": company,
                        "Job Role": title,
                        "Location": location,
                        "Job Link": link,
                        "Job Description": description,
                    })
                except Exception:
                    continue
            try:
                pane = driver.find_element(By.CSS_SELECTOR, 'div.scaffold-layout__list')
                next_btn = pane.find_element(By.CSS_SELECTOR, 'button.jobs-search-pagination__button--next')
                if "disabled" in next_btn.get_attribute("class"):
                    break
                next_btn.click()
                human_delay()
            except Exception:
                break
    finally:
        driver.quit()
    return results