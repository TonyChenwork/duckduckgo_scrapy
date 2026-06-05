from playwright.sync_api import sync_playwright
import csv

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        with open("keywords.txt","r",encoding="utf-8") as f:
            keywords = [line.strip() for line in f if line.strip()]  

        with open("data.csv","w",newline="",encoding="UTF-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["keyword","rank","title","link"])


            for keyword in keywords:
 
                page.goto("https://duckduckgo.com/")

                page.fill('input[name="q"]',keyword)
                page.press("#searchbox_input","Enter")

                try:
                    page.wait_for_selector('a[data-testid="result-title-a"]',timeout=10000)
                except:
                    writer.writerow([keyword,"FAILED","No results or timeout",""])
                    continue

                results = page.locator('a[data-testid="result-title-a"]').all()[:5]
                rank = 0

                for rank,r in enumerate (results, start=1):
                    title = r.text_content()
                    link = r.get_attribute("href")
                    

                    writer.writerow([keyword,rank,title,link])
            
        browser.close()

run()