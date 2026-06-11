from playwright.sync_api import sync_playwright
import csv

#读取定义函数（）里的文件并且去掉空行
def read_keywords(filename):
    with open(filename,"r",encoding="utf-8") as f:
        keywords = [line.strip() for line in f if line.strip()] 
    return keywords

#前往duckduckgo网页，在输入框输入定义函数（）里的keyword并等待网页结果加载完毕（最多等10秒）
def search_keyword(page,keyword):
    page.goto("https://duckduckgo.com/")
    page.fill('input[name="q"]',keyword)
    page.press("#searchbox_input","Enter")

    page.wait_for_selector('a[data-testid="result-title-a"]',timeout=10000)

# 抓取当前搜索结果页的标题链接元素，按排名提取 title 和 link，并返回 rows 列表
def scrape_results(page,keyword,max_results=10):
    results = page.locator('a[data-testid="result-title-a"]').all()[:max_results]
    
    rows = []

    for rank,result in enumerate (results, start=1):
        title = result.text_content().strip()
        link = result.get_attribute("href")

        rows.append([keyword,rank,title,link])
    
    return rows

# 循环点击“更多结果”按钮，并等待搜索结果数量增加
def load_more_results(page, times):
    for i in range(times):
        try:
            more_button = page.locator("#more-results")

            if more_button.count() == 0:
                print("No More Results button found.")
                break

            old_count = page.locator('a[data-testid="result-title-a"]').count()
            print(f"Clicking more results... current results: {old_count}")

            more_button.click()

            page.wait_for_function(
                """oldCount => {
                    return document.querySelectorAll('a[data-testid="result-title-a"]').length > oldCount
                }""",
                arg=old_count,
                timeout=10000
            )

            new_count = page.locator('a[data-testid="result-title-a"]').count()
            print(f"Loaded more results: {old_count} -> {new_count}")

        except Exception as e:
            print(f"Failed to load more results: {e}")
            break

#用read_keywrods定义keywords,打开playwright，创建csv，用search_keywords和scrape_results循环keywords，先加载后用rows存入爬取的title和link数据，把数据循环写入csv，最后用try:except提取报错信息
def run():
    keywords = read_keywords("keywords.txt")

    try:
        max_pages = int(input("max pages per keword: "))
        max_results = int(input("max results per keyword: "))
    except ValueError:
        print("Please enter vail numbers.")
        return
    
    if max_pages < 1 or max_pages >5:
        print("Please enter max_page between 1 and 5.")
        return
    
    if max_results < 1 or max_results > 50:
        print("Please enter max_results between 1 and 50.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page() 

        with open("data.csv","w",newline="",encoding="UTF-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["keyword","rank","title","link"])

            for keyword in keywords:
                print(f"Searching: {keyword}")

                try:
                    search_keyword(page,keyword)

                    if max_pages > 1:
                        load_more_results(page,max_pages -1)

                    rows = scrape_results(page,keyword,max_results=max_results)

                    for row in rows:
                        writer.writerow(row)

                    print(f"Scraped {len(rows)} results for: {keyword}")

                except Exception as e:
                    writer.writerow([keyword,"FAILED",f"No results or error: {e}",""])
                    print(f"Failed: {keyword} | Error: {e}")
            
        browser.close()

run()