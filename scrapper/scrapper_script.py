from playwright.sync_api import sync_playwright
import pandas as pd

# Base URL pattern with page offset
BASE_URL = "https://www.indiacode.nic.in/handle/123456789/2516/simple-search?location=123456789/2516&query=&sort_by=score&order=desc&rpp=100&etal=0&start={}"

# Change this depending on how many pages you want (0, 100, 200, ...)
PAGE_OFFSETS = [0, 100, 200, 300]  # Each offset = page start index

def scrape_table(page):
    """Extracts table data and links from the current page."""
    data = []
    table = page.locator("table.table-hover")
    
    # Extract headers and add 'Link' column
    headers = table.locator("th").all_text_contents()
    headers.append("Link")
    
    # Extract rows
    row_count = table.locator("tbody tr").count()
    for i in range(row_count):
        row_data = []
        link_url = None
        
        cell_count = table.locator(f"tbody tr:nth-child({i+1}) td").count()
        for j in range(cell_count):
            cell = table.locator(f"tbody tr:nth-child({i+1}) td:nth-child({j+1})")
            text = cell.inner_text().strip()
            
            # If there's an <a> tag inside, grab href
            link = cell.locator("a")
            if link.count() > 0:
                href = link.first.get_attribute("href")
                if href:
                    link_url = "https://www.indiacode.nic.in" + href
            
            row_data.append(text)
        
        # Add link as last column
        row_data.append(link_url)
        data.append(row_data)
    
    return headers, data

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    all_data = []
    headers = None
    
    for offset in PAGE_OFFSETS:
        page_url = BASE_URL.format(offset)
        print(f"📄 Scraping page starting at {offset} → {page_url}")
        
        page.goto(page_url)
        page.wait_for_selector("table.table-hover")
        
        headers, page_data = scrape_table(page)
        all_data.extend(page_data)
    
    browser.close()
    
    df = pd.DataFrame(all_data, columns=headers)
    df.to_csv("kerala_acts_paginated.csv", index=False)
    print(f"✅ Scraped {len(df)} rows across {len(PAGE_OFFSETS)} pages and saved to kerala_acts_paginated.csv")
