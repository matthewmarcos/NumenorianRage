from scrapy import Request, Spider
import csv
import json
import os
from CharacterParser import CharacterParser

"""
Cool Stuff
"""
class NumenorianKingsScraper(Spider):
    name = 'numenorian_kings_scraper'
    output_file = 'kings.txt'
    start_urls = [
        'http://tolkiengateway.net/wiki/King_of_N%C3%BAmenor'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        BASE_URL = 'http://tolkiengateway.net'
        table_selector = '#mainContent table'

        kings_table_rows = response.css(table_selector)[0].css('tr')
        for king_table_row in kings_table_rows[2:]:
            [sNumber, sLink, sReign, sNotes] = king_table_row.css('td')
            king_profile_url = BASE_URL + sLink.css('a').attrib['href']
            # self.write_to_file(king_profile_url)
            CharacterParser.scrape_character(king_profile_url)
    
    def get_element(self, selector, path):
        return selector.css(path)

    def write_to_file(self, content_string):
        with open(self.output_file, 'a') as fp:
            fp.write(content_string)
            fp.write('\n')
