from csv import DictWriter
from operator import itemgetter
from scrapy import Request, Spider
import re
import unicodedata


class FamilyScraper(Spider):
    """ Scrapes
        Scrapes information about each member of the Numenorian Royal
        Family Tree
    """

    name = 'numenorian_kings_scraper'
    output_file = 'numenorians.psv'
    start_urls = [
        # Numenorian Kings
        'http://tolkiengateway.net/wiki/Elros',
        # Royal bloodline of Arnor and Gondor
        'http://tolkiengateway.net/wiki/Elendil'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, meta={'depth': 1})

    def parse(self, response):
        BASE_URL = 'http://tolkiengateway.net'
        table_selector = '#mainContent table'
        tables = response.css(table_selector)
        url = response.url
        main_table = self.get_main_table(tables)
        table_rows = main_table.css('tr')

        profile = {
            'url': url,
            'referrer': response.request.headers.get('Referer', None),
            'name': '',
            'other_names': '',
            'titles': '',
            'birth_year': None,
            'rule_start': None,
            'rule_end': None,
            'death_year': None,
            'notable_for': '',
            'children': '',
        }

        for idx, table_row in enumerate(table_rows):
            td_list = []

            if(idx == 0):
                profile['name'] = table_row.css('th::text').get()

            td_list = table_row.css('td')

            if(len(td_list) != 2):
                continue

            row_label = unicodedata.normalize(
                'NFKC',
                td_list.css('td:first-child::text').get() or 'default'
            )

            key = {
                'Other names': 'other_names',
                'Titles': 'titles',
                'Birth': 'birth_year',
                'Rule': 'rule_start',
                'Death': 'death_year',
                'Notable For': 'notable_for',
                'Children': 'children',
                'default': ''
            }.get(row_label, '')

            profile = self.extract_row_value(profile, td_list, key)

        self.save_profile(profile)
        for child_url in profile['children']:
            yield Request(url=BASE_URL + child_url,
                          callback=self.parse,
                          meta={'depth': response.meta['depth'] + 1})

    def extract_row_value(self, profile, td_list, key):
        value_col = td_list.css('td:nth-child(2)')

        if key in set([
            "titles",
            "notable_for",
            "other_names"
        ]):
            profile[key] = (
                self.extract_text(value_col))

        elif key in set([
            "birth_year",
            "rule_start",
            "death_year"
        ]):
            profile[key] = (
                self.extract_date(value_col))

        elif key == "children":
            profile[key] = (
                [child_link.attrib['href']
                    for child_link in self.extract_children(value_col)])

        return profile

    def get_main_table(self, tables_selector):
        tables = [(table_selector, len(table_selector.css('tr').getall()))
                  for table_selector in tables_selector]

        # Weird pattern I found on the pages. We got the Numenorian Kings
        # and members of the royal bloodline
        if(len(tables_selector) < 5):
            return tables_selector[0]

        # We know for certain that the main table is the largest of the
        # first 2 tables.
        return max(tables[:2], key=itemgetter(1))[0]

    def extract_text(self, selector):
        return selector.css('::text').get()

    def extract_date(self, selector):
        birth_string = ''.join(selector.css('::text').getall())
        return re.split(r"  ", birth_string)[0]

    # def extract_notable_for(self, selector):
    #     return selector.css('::text').get()

    def extract_children(self, selector):
        return selector.css('td>a')

    def get_element(self, selector, path):
        return selector.css(path)

    def save_profile(self, profile):
        headers = [
            'url',
            'referrer',
            'name',
            'other_names',
            'titles',
            'birth_year',
            'rule_start',
            'rule_end',
            'death_year',
            'notable_for'
        ]

        to_save = {header: profile[header] for header in headers}

        with open(self.output_file, 'a+') as fp:
            dict_writer = DictWriter(fp, delimiter='|', fieldnames=headers)
            dict_writer.writerow(to_save)
