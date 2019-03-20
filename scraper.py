"""
how to run script
cmd line
dir  = PycharmProjects\twitter_bot\quote_scraper
# crawl
scrapy runspider scraper.py
# save as X.json
scrapy runspider scraper.py -o pick_name.json
scrapy runspider scraper.py -o friedrich_nietzsche_quotes.json
"""

import scrapy
from detect_english import is_english


class QuotesSpider(scrapy.Spider):
    name = "quote_scraper"
    start_urls = ['https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=FRIEDRICH+NIETZSCHE&commit=Search']

    def parse(self, response):

        # get author name
        for x in response.css('.desktop'):
            NAME_SELECTOR = 'head title ::text'
            author = x.css(NAME_SELECTOR).extract_first()
            author = author.split()
            author = author[-2] +' '+ author[-1]
            author = author.strip("'")
            author = author.strip("'.")
            #soren kierkgaard only
            #author = author.replace('ø', 'o')
            break

        # get quote information
        SET_SELECTOR = '.quoteText'
        for quotes in response.css(SET_SELECTOR):
            NAME_SELECTOR = '::text'
            raw_text = quotes.css(NAME_SELECTOR).extract_first().strip()

            # check if text is english
            if is_english(raw_text) == False:
                continue
            # check if text is too long for twitter
            if len(raw_text) >= 280:
                continue

            yield {'quote': raw_text.strip('“' '”' u'…' u'—' u'’'),
                   'author': author}

        #"""
        # go to next page
        NEXT_PAGE_SELECTOR = '.next_page ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
        #"""






"""
links used

#jean paul sartre
https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=Jean-Paul+Sartre&commit=Search
# albert camus
https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=albert+camus&commit=Search
# Martin Heidegger
https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=martin+heidegger&commit=Search
#FYODOR DOSTOEVSKY
https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=fyodor+dostoevsky&commit=Search
#FRIEDRICH NIETZSCHE
https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=FRIEDRICH+NIETZSCHE&commit=Search
"""