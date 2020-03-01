# Numenorian Rage

Scrapes the family line of Elros and Elendil from [http://tolkiengateway.net/](http://tolkiengateway.net/), cleans the data, and provides an analysis on their lifespans.

## Instructions
### Running the scraper
1. Make your own `.env` file based on the provided `.env.sample`
1. Install `scrapy`
1. Run `scrapy runspider FamilyScraper.py` to start crawling.

### Cleaning the data
1. Run `python CleanKingsData.py`

### Running the notebook
1. Run `jupyter notebook`
