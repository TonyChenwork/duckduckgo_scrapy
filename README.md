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
