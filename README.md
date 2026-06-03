# DuckDuckGo Search Scraper

A simple web automation and scraping project built with Python and Playwright.

This scraper opens DuckDuckGo, searches for a user-provided keyword, extracts search result titles and links, and exports the results into a CSV file.

## Features

* Open DuckDuckGo automatically
* Accept a search keyword from user input
* Fill the search box automatically
* Press Enter to search
* Wait for search results to load
* Extract result titles
* Extract result links
* Export results to CSV format

## Technologies

* Python
* Playwright
* CSV

## Output Fields

| Field   | Description                            |
| ------- | -------------------------------------- |
| keyword | The search keyword entered by the user |
| title   | Search result title                    |
| link    | Search result URL                      |

## Version History

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

The main goal is to practice browser interaction, including filling input fields, pressing keys, waiting for dynamic search results, extracting structured data, and exporting clean results into a CSV file.
