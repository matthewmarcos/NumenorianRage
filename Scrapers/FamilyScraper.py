from scrapy import Request, Spider
# from scrapy.Selector import HtmlXPathSelector
import csv
import json
import os
from CharacterParser import CharacterParser

"""
Cool Stuff
"""
class FamilyScraper(Spider):
    name = 'numenorian_kings_scraper'
    output_file = 'kings.txt'
    start_urls = [
        'http://tolkiengateway.net/wiki/Elros',  # Numenorian Kings 
        # 'http://tolkiengateway.net/wiki/Elendil'  # Royal bloodline of Arnor and Gondor
    ]

    table_label_mapping = {
        # Other Names
        'Other names': 'other_names',
        # Get Title (If any)
        'Titles': 'titles',
        # Birth
        'Birth': 'birth',
        # Rule
        'Rule': 'rule',
        # Death 
        'Death': 'death',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        BASE_URL = 'http://tolkiengateway.net'
        table_selector = '#mainContent table'

        table_rows = response.css(table_selector)[1].css('tr')

        url = response.url
        name = ''
        title = ''
        other_names = ''
        birth_year = None
        rule_start = None
        rule_end = None
        death_year = None
        notable_for = ''
        
        for idx, table_row in enumerate(table_rows):
            # Get Name
            if(idx == 0):
                name = table_row.css('th').get()
            
            td_list = table_row.css('td')
            pass
            # Other Names
            # Get Title (If any)
            # Birth
            # Rule
            # Death 
    
    def get_element(self, selector, path):
        return selector.css(path)

    def write_to_file(self, content_string):
        with open(self.output_file, 'a') as fp:
            fp.write(content_string)
            fp.write('\n')
