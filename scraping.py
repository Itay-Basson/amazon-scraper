import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from database import insert_search_history







def get_amazon_com_search_results(search_query: str):
    service = Service()
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.com")

    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )

    search_box.send_keys(search_query)
    search_box.submit()

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".s-result-item"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    results = []

    for item in soup.select(".s-result-item"):
        title = item.select_one(".a-link-normal .a-size-medium, .a-link-normal .a-text-normal")
        image = item.select_one(".s-image")
        asin = item.get("data-asin")
        if title and image and asin:
            results.append({
                "asin": asin,
                "name": title.text.strip(),
                "image_url": image["src"]
            })

    return results[:10]

def get_product_details(asin: str, base_url: str = "https://www.amazon.com"):
    url = f"{base_url}/dp/{asin}"
    service = Service()
    driver = webdriver.Chrome()
    driver.get(url)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#productTitle"))
    )

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@class, 'a-price') and not(contains(@class, 'a-text-strike'))]")
            )
        )
    except TimeoutException:
        pass

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    name = soup.select_one("#productTitle").text.strip()
    rating = (
        soup.select_one("#acrPopover")["title"].strip()
        if soup.select_one("#acrPopover")
        else "No rating available"
    )

    price_element = soup.select_one(
        "span.a-price:not(.a-text-strike) > span.a-offscreen"
    )
    price = price_element.text.strip() if price_element else "No price available"

    return {"name": name, "rating": rating, "price": price}

def get_exchange_rates():
    url = "https://www.x-rates.com/calculator/?from=USD&to=EUR&amount=1"
    currencies = ["GBP", "CAD", "EUR"]
    exchange_rates = {"USD": 1}

    for currency in currencies:
        response = requests.get(f"https://www.x-rates.com/calculator/?from=USD&to={currency}&amount=1")
        soup = BeautifulSoup(response.text, "html.parser")
        rate = float(soup.select_one(".ccOutputTrail").previous_sibling.string)
        exchange_rates[currency] = rate

    return exchange_rates

def convert_to_usd(price, from_currency, exchange_rates):
    if not price:
        return None
    price = price.replace('$', '').replace('€', '').replace('£', '')
    usd_rate = exchange_rates.get(from_currency, None)
    if usd_rate:
        return round(float(price) / usd_rate, 2)
    return None


def get_product_details_parallel(asin: str):
    amazon_sites = {
        "https://www.amazon.com": "USD",
        "https://www.amazon.co.uk": "GBP",
        "https://www.amazon.ca": "CAD",
        "https://www.amazon.de": "EUR",
    }

    exchange_rates = get_exchange_rates()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_product_details, asin, site): site for site in amazon_sites}
        results = {}
        name, rating = None, None

        for future in concurrent.futures.as_completed(futures):
            site = futures[future]
            try:
                result = future.result()
                if site == "https://www.amazon.com":
                    name, rating = result["name"], result["rating"]
                price_usd = convert_to_usd(result["price"], amazon_sites[site], exchange_rates)
                results[site] = price_usd
            except Exception as e:
                print(f"Error fetching product details for {site}: {e}")
                results[site] = None
        # Save the relevant data to the search_history table
    search_history_data = {
        'name': name,
        'asin': asin,
        'amazon_us': results['https://www.amazon.com'],
        'amazon_uk': results['https://www.amazon.co.uk'],
        'amazon_de': results['https://www.amazon.de'],
        'amazon_ca': results['https://www.amazon.ca'],
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    insert_search_history(search_history_data)

    return {"name": name, "rating": rating, "prices": results}










