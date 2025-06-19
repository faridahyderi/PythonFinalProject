import os
import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up headless Chrome with custom user-agent
options = Options()
options.add_argument("--headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/114.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)  # 30 seconds page load timeout

# Years to scrape: 2006 to 2009 inclusive
years = list(range(2006, 2010))

# Create output directory if not exists
os.makedirs("output", exist_ok=True)

max_retries = 3

for year in years:
    print(f"\n[+] Scraping year {year}...")
    url = f"https://www.baseball-almanac.com/yearly/yr{year}a.shtml"

    for attempt in range(max_retries):
        try:
            driver.get(url)
            break  # success
        except Exception as e:
            print(f"Timeout loading {url}, retry {attempt+1}/{max_retries}")
            if attempt == max_retries - 1:
                print(f"Failed to load {url} after {max_retries} attempts. Skipping year.")
                continue  # skip this year
            time.sleep(5)  # wait before retry

    else:
        # If all retries failed, skip to next year
        continue

    # Polite random delay before scraping tables
    time.sleep(3 + random.random() * 2)  # 3 to 5 seconds

    tables = driver.find_elements(By.TAG_NAME, "table")

    for idx, table in enumerate(tables, start=1):
        # Try to extract heading above the table
        try:
            heading = table.find_element(By.XPATH, "./preceding-sibling::h2[1] | ./preceding-sibling::h3[1]")
            section_title = heading.text.strip()
        except:
            section_title = f"table_{idx}"

        # Create safe filename
        safe_title = section_title[:40].replace(" ", "_").replace("/", "-")
        filename = f"{year}_{idx:02d}_{safe_title}.csv"
        filepath = os.path.join("output", filename)

        rows = table.find_elements(By.TAG_NAME, "tr")
        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "th") + row.find_elements(By.TAG_NAME, "td")
            # Keep empty cells for consistent CSV structure
            row_data = [cell.text.strip() for cell in cells]
            if any(cell != "" for cell in row_data):  # skip fully empty rows
                data.append(row_data)

        if data:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            print(f"Saved {len(data)} rows to {filename}")
        else:
            print(f"Skipped empty table: {filename}")

print("\nFinished scraping all years.")
driver.quit()
