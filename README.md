# Númenórian Rage

Scrapes the family line of Elros and Elendil from [http://tolkiengateway.net/](http://tolkiengateway.net/), cleans the data, and provides an analysis on their lifespans.

This project is currently a work in progress.

## Prerequisites
This project was made with Python 3.8

```
conda create --name numenor
source activate numenor
pip install pandas matplotlib scrapy jupyter
```
I have included a requirements.txt if you want to use the exact versions I have.

`pip install -r requirements.txt`

## Running the scraper
You can gather the raw data by scraping through the tolkiengateway website.

`scrapy runspider FamilyScraper.py`

## Cleaning the data
Scraping is not always produce ready-to-use results. You have to clean the data.

`python CleanKingsData.py`

## Running the notebook
Run the jupyter notebook to see my analysis and insights on the Númenórians.

`jupyter notebook`
