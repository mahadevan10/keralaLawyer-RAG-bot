import os
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Load CSV
csv_file = "kerala_acts_paginated.csv"
df = pd.read_csv(csv_file)

# Ensure PDFs folder exists
pdf_dir = "pdfs"
os.makedirs(pdf_dir, exist_ok=True)

# Track already downloaded PDFs
downloaded_files = set(os.listdir(pdf_dir))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Change to True for silent run
    page = browser.new_page()

    for i, row in df.iterrows():
        url = str(row["Link"]).strip()
        if not url.startswith("http"):
            continue

        # Create a unique filename from Act Number + Short Title
        safe_name = row["Short Title"].replace(" ", "_").replace("/", "_")
        filename = f"{row['Act Number']}_{safe_name}.pdf"
        filepath = os.path.join(pdf_dir, filename)

        # Skip if already downloaded
        if filename in downloaded_files:
            print(f"Skipping (already downloaded): {filename}")
            continue

        print(f"Opening: {url}")
        try:
            page.goto(url, timeout=60000)

            # Find the PDF link inside container
            link_el = page.query_selector('div.container a[target="_blank"]')
            if link_el:
                pdf_link = link_el.get_attribute("href").strip()
                if pdf_link.startswith("/"):
                    pdf_link = "https://www.indiacode.nic.in" + pdf_link

                print(f"Downloading PDF: {pdf_link}")
                pdf_bytes = page.context.request.get(pdf_link).body()

                with open(filepath, "wb") as f:
                    f.write(pdf_bytes)
                print(f"Saved: {filepath}")
            else:
                print(f"No PDF found at {url}")

        except PlaywrightTimeout:
            print(f"Timeout on: {url} — skipping to next")
        except Exception as e:
            print(f"Error on {url}: {e}")

    browser.close()
