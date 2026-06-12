from playwright.sync_api import sync_playwright
import csv

#读取 keywords.txt文件，去掉空行，返回关键词列表
def read_keywords(filename):
    with open(filename,"r",encoding="utf-8") as f:
        keywords = [line.strip() for line in f if line.strip()] 
    return keywords

#前往页面，搜索一个关键词，等待内容加载
def search_keyword(page,keyword):
    page.goto("https://duckduckgo.com/")
    page.fill('input[name="q"]',keyword)
    page.press("#searchbox_input","Enter")

    page.wait_for_selector('a[data-testid="result-title-a"]',timeout=10000)

#从当前搜索结果页提取 title 和 link，按 rank 组成rows 列表并返回。
def scrape_results(page,keyword,max_results=10):
    results = page.locator('a[data-testid="result-title-a"]').all()[:max_results]
    
    rows = []

    for rank,result in enumerate (results, start=1):
        title = result.text_content().strip()
        link = result.get_attribute("href")

        rows.append([keyword,rank,title,link])
    
    return rows

#按下times次“更多结果”按钮，并等待数据加载完毕，输出新的数据数量结果。
def load_more_results(page, times):
    for i in range(times):
        try:
            more_button = page.locator("#more-results")
            
            #判断是否还有“更多结果”按钮
            if more_button.count() == 0:
                print("No More Results button found.")
                break

            #存入点击“更多结果”按钮前的数据数量
            old_count = page.locator('a[data-testid="result-title-a"]').count()
            print(f"Clicking more results... current results: {old_count}")
            
            #点击按钮
            more_button.click()

            #等待JS返回所有标题数量大于按按钮前的标题熟练是True的时候
            page.wait_for_function(
                """oldCount => {
                    return document.querySelectorAll('a[data-testid="result-title-a"]').length > oldCount
                }""",
                arg=old_count,
                timeout=10000
            )
            
            #存入按完按钮后的标题数量
            new_count = page.locator('a[data-testid="result-title-a"]').count()
            print(f"Loaded more results: {old_count} -> {new_count}")
        
        #报错输出报错内容
        except Exception as e:
            print(f"Failed to load more results: {e}")
            break

#主流程：读取数据存入列表 -> 输入最大页数和最多结果 -> 判断输入值是否“合法” -> 打开playwright，创建CSV -> 使用scrape_results()函数搜索，如果page > 1则使用load_more_results函数加载更多，写入csv文件。-> 如果某个关键词失败，记录报错继续下一个关键词。
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