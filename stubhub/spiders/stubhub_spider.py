import json
import scrapy
from stubhub.items import StubHubItem


class StubHub(scrapy.Spider):
    name = 'stubhub'

    def start_requests(self):
        start_urls = [
            'https://www.stubhub.com/melissa-etheridge-nashville-tickets-10-5-2025/event/158435406/'
        ]
        for base_url in start_urls:
            starting_page = 0
            yield scrapy.Request(
                url=base_url,
                meta={
                    "base_url": base_url,
                    "quantity": starting_page
                },
                callback=self.parse
            )

    def parse(self, response, **kwargs):
        quantity = response.meta["quantity"]
        item = StubHubItem()
        tickets_data = response.css('#index-data ::text').get()
        tickets_data = json.loads(tickets_data)
        tickets = tickets_data['grid']['items']
        for ticket in tickets:
            item['id'] = ticket.get('id')
            item['eventId'] = ticket.get('eventId')
            item['section'] = ticket.get('section')
            item['sectionMapName'] = ticket.get('sectionMapName')
            item['row'] = ticket.get('row')
            item['seat'] = ticket.get('seat')
            item['seatFrom'] = ticket.get('seatFrom')
            item['seatTo'] = ticket.get('seatTo')
            item['seatFromInternal'] = ticket.get('seatFromInternal')
            item['availableTickets'] = ticket.get('availableTickets')
            yield item

        remaining_items = tickets_data['grid'].get('itemsRemaining')
        if remaining_items and remaining_items > 0:
            quantity += 1
            base_url = response.meta['base_url']
            next_page_url = f'{base_url}?quantity={quantity}'
            yield scrapy.Request(
                url=next_page_url,
                meta={
                    "base_url": base_url,
                    "quantity": quantity
                },
                callback=self.parse
            )
