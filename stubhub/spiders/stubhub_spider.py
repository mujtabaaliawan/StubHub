import json
import math
from json import JSONDecodeError

import scrapy
from stubhub.items import StubHubItem


class StubHub(scrapy.Spider):
    name = 'stubhub'

    def start_requests(self):
        with open('link_urls.json') as f:
            data = json.load(f)
            start_urls = data.get("urls", [])

        for base_url in start_urls:
            current_page = 0
            yield scrapy.Request(
                url=f'{base_url}?quantity={current_page}',
                meta={
                    "base_url": base_url,
                    "current_page": current_page
                },
                callback=self.parse
            )

    def parse(self, response, **kwargs):
        current_page = response.meta["current_page"]
        try:
            tickets_data = response.css('#index-data ::text').get()
            if not tickets_data:
                self.logger.warning("No ticket data found on page %s", current_page)
                return

            tickets_data = json.loads(tickets_data)
            tickets = tickets_data['grid']['items']
            for ticket in tickets:
                item = StubHubItem()
                item['id'] = ticket.get('id')
                item['eventId'] = ticket.get('eventId')
                item['section'] = ticket.get('section')
                item['sectionMapName'] = ticket.get('sectionMapName')
                item['row'] = ticket.get('row')
                item['seat'] = ticket.get('seat')
                item['seatFrom'] = ticket.get('seatFrom')
                item['seatTo'] = ticket.get('seatTo')
                item['seatFromInternal'] = ticket.get('seatFromInternal')
                available_tickets = ticket.get('availableTickets')
                if not available_tickets:
                    # website not displaying whose available tickets are 0
                    continue
                item['availableTickets'] = ticket.get('availableTickets')
                yield item

            total_listings = tickets_data.get('totalListings', 0)
            if total_listings:
                listings_per_page = 21
                total_pages = math.ceil(total_listings / listings_per_page)
                current_page += 1
                if total_pages and current_page < total_pages:
                    base_url = response.meta['base_url']
                    next_page_url = f'{base_url}?quantity={current_page}'
                    yield scrapy.Request(
                        url=next_page_url,
                        meta={
                            "base_url": base_url,
                            "current_page": current_page
                        },
                        callback=self.parse
                    )

        except JSONDecodeError as jd:
            self.logger.error("JSON decode error on page %s: %s", current_page, jd)

        except Exception as e:
            self.logger.error("Unhandled error on page %s: %s", current_page, e, exc_info=True)
