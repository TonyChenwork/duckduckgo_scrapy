from playwright.sync_api import sync_playwright
import csv

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://duckduckgo.com/")

        keyword = input("Serch Keyword: ")

        page.fill('input[name="q"]',keyword)
        page.press("#searchbox_input","Enter")

        page.wait_for_selector('a[data-testid="result-title-a"]')

        results = page.locator('a[data-testid="result-title-a"]').all()

        with open("data.csv","w",newline="",encoding="UTF-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["keyword","title","link"])

            for r in results:
                title = r.text_content()
                link = r.get_attribute("href")

                writer.writerow([keyword,title,link])
            
        browser.close()

run()