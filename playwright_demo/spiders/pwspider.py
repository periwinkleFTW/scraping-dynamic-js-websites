import scrapy
from scrapy_playwright.page import PageCoroutine


class PwspiderSpider(scrapy.Spider):
    name = 'pwspider'

    def start_requests(self):
        yield scrapy.Request('https://twitter.com',
                             meta=dict(
                                 playwright=True,
                                 playwright_include_page=True,
                                 playwright_page_coroutines=[
                                     # This where we can implement scrolling if we want
                                     PageCoroutine(
                                         'wait_for_selector', 'div#itemName')
                                 ]
                             )
                             )

    async def parse(self, response):
        for item in response.css('div.card'):
            yield {
                'name': item.css('h3::text').get(),
                'price': item.css('div.form-group label::text').get()
            }
