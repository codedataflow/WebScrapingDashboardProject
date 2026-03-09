import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def build_driver() -> webdriver.Chrome:
    """Return a headless Chrome driver with realistic user-agent headers."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    return driver

def safe_text(element) -> str:
    try:
        return element.text.strip()
    except Exception:
        return ""

def parse_table(table, idxs: int, start: int = 0) -> list:
    rows = []
    trs = table.find_elements(By.TAG_NAME, "tr")
    keys = trs[1].find_elements(By.TAG_NAME, "td")
    rng = range(start, idxs)
    rowspan_dict = {}

    dict_keys = []
    for i in rng:
        dict_keys.append(safe_text(keys[i]))

    for tr in trs[2:-2]:
        tds = tr.find_elements(By.CSS_SELECTOR, "td[class^='datacol']")

        if len(tds) == 0:
            continue

        offset = 0
        rows_dict = {}
        for i in rng:
            idx = i-start
            if idx in rowspan_dict and rowspan_dict[idx][0] > 1:
                rows_dict[dict_keys[idx]] = rowspan_dict[idx][1]
                rowspan_dict[idx][0] -= 1
                offset += 1
                if rowspan_dict[idx][0] < 1:
                    offset = 0
                    rowspan_dict = {}
            else:
                rows_dict[dict_keys[idx]] = safe_text(tds[idx-offset])

        rows.append(rows_dict)
        if len(tds) >= idxs:
            for i in rng:
                idx = i-start
                rowspan = tds[idx].get_attribute("rowspan")
                if rowspan:
                    rowspan_count = int(rowspan)
                    rowspan_dict[i-start] = [rowspan_count, safe_text(tds[idx])]

    return rows

def scrape_statistics(driver: webdriver.Chrome, year: int) -> tuple[list, list, list]:
    # pre-requisite: first table is a players, second - pitchers, third - team_standings
    try:
        driver.get(f"https://www.baseball-almanac.com/yearly/yr{year}a.shtml")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "table")))

        tables = driver.find_elements(By.TAG_NAME, "table")
        if len(tables) >= 2:
            return [parse_table(tables[0], 4), parse_table(tables[1], 4), parse_table(tables[2], 6, 1)]

    except TimeoutException:
        print(f"  [WARN] Timeout loading year {year}")
    except Exception as e:
        print(f"  [WARN] Error scraping year {year}: {e}")

    return None

def main():
    years = list(range(2020, 2025))
    print("Starting MLB History Scraper…")
    driver = build_driver()
    statistics = {'players': [], 'pitchers': [], 'team_standings': []}

    try:
        for year in years:
            print(f"Scraping year {year}…")

            stats = scrape_statistics(driver, year)
            if stats != None:
                year_row = {'Year': year}
                # statistics[year] = {'players': stats[0], 'pitchers': stats[1], 'team_standings': stats[2]}
                [row.update(year_row) for row in stats[0]]
                [row.update(year_row) for row in stats[1]]
                [row.update(year_row) for row in stats[2]]
                statistics['players'] += stats[0]
                statistics['pitchers'] += stats[1]
                statistics['team_standings'] += stats[2]
    finally:
        driver.quit()
    
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    for key in statistics.keys():
        data = pd.DataFrame(statistics[key])
        print(data)
        csv_path = f"{output_dir}/{key}.csv"
        data.to_csv(csv_path, index=False)
        print(f"Saved {key} data ({len(data)} rows) to {csv_path}")

    print("Scraping complete! Files saved")

if __name__ == "__main__":
    main()
