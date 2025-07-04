# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StubHubItem(scrapy.Item):

    id = scrapy.Field()
    eventId = scrapy.Field()
    section = scrapy.Field()
    sectionMapName = scrapy.Field()
    row = scrapy.Field()
    seat = scrapy.Field()
    seatFrom = scrapy.Field()
    seatTo = scrapy.Field()
    seatFromInternal = scrapy.Field()
    availableTickets = scrapy.Field()
