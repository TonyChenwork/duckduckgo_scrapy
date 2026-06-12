# DuckDuckGo Search Scraper

A simple web automation and scraping project built with Python and Playwright.

This scraper opens DuckDuckGo, reads multiple keywords from a text file, searches each keyword automatically, extracts the top search result titles and links, and exports the results into a CSV file.

## Features

* Open DuckDuckGo automatically
* Read multiple keywords from `keywords.txt`
* Search each keyword automatically
* Fill the search box automatically
* Press Enter to search
* Wait for search results to load
* Extract result titles
* Extract result links
* Export results to CSV format
* Add ranking number for each result
* Configure maximum results per keyword
* Configure maximum pages per keyword
* Load more DuckDuckGo results with the `#more-results` button
* Basic error handling for failed searches

## Technologies

* Python
* Playwright
* CSV

## Input File

The scraper reads keywords from a text file named:

```text
keywords.txt
```

Example:

```text
cologne
Bali
digital nomad
```

## Output Fields

| Field   | Description                               |
| ------- | ----------------------------------------- |
| keyword | The search keyword                        |
| rank    | The ranking position of the search result |
| title   | Search result title                       |
| link    | Search result URL                         |

## Version History

### v1.6

* Added code structure comments for all main functions
* Added a mind map to explain the full scraper workflow
* Reviewed the relationship between `max_pages` and `max_results`
* Tested multiple configurations for first-page and load-more scraping
* Confirmed CSV output structure with non-empty keyword, rank, title, and link fields

### v1.5

* Refactored scraper into reusable functions
* Added configurable `max_pages` per keyword
* Added configurable `max_results` per keyword
* Added experimental "More Results" loading with the `#more-results` button
* Added result count checking before and after loading more results
* Added basic error handling for failed searches and loading failures

### v1.4

* Added rank field to the CSV output
* Limited each keyword to the top 5 search results
* Improved output structure for easier review

### v1.3

* Added support for reading keywords from `keywords.txt`
* Skipped empty lines in the keyword file

### v1.2

* Added batch keyword search support
* Searched multiple keywords automatically
* Exported all keyword results into one CSV file

### v1.1

* Added user keyword input
* Exported keyword, title and link to CSV
* Improved selector strategy by using stable attributes such as `name`, `id`, and `data-testid`

### v1.0

* Opened DuckDuckGo automatically
* Searched a fixed keyword
* Extracted first-page result titles and links
* Exported results to CSV format

## Notes

This project is a beginner-friendly Playwright automation project.

The main goal is to practice browser interaction, including filling input fields, pressing keys, waiting for dynamic search results, extracting structured data, handling batch input, loading more results, adding basic error handling, and exporting clean results into a CSV file.

This project follows a common search scraping workflow:

Keyword list → Search page → Load more results → Structured CSV output


## Validation Notes

For this beginner scraper, validation focuses on:

* CSV is generated successfully
* Each row has a keyword, rank, title, and link
* Empty lines in `keywords.txt` are skipped
* `max_results` works as an upper limit per keyword
* `max_pages` controls how many result batches are loaded
* Failed searches are recorded instead of stopping the whole program

Manual checking of every search result URL is not required for this stage.

# Mind map

run()
|
read_keywords("keywords.txt")
|         |-return keywords
|
|-input max_pages, max_results
|
|-validate max_pages, max_results
|
|-open Playwright browser
|-create CSV writer
|
|-for keyword in keywords:
    |
    |-try:
        |-search_keyword(page,keyword)
        |   |-open website and search keyword
        |   |-wait for results
        |
        |-if max_pages > 1:
        |   |-load_more_results(page,max_pages - 1)
        |           |-click '#more-results'
        |           |-wait until result count increases
        |
        |-rows = scrape_results(page,keyword,max_results)
        |   |-extract title and link
        |   |-return rows
        |
        |-for row in rows:
        |   |-writer.writerow(row)
    |
    |-except:
        |-write error in CSV
        |-print the error
|
browser.close()
           