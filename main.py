from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from stubhub.spiders.stubhub_spider import StubHub


def run_spider(spider_cls):
    settings = get_project_settings().copy()
    output_filename = f"{spider_cls.name}_results.json"
    settings.set('FEEDS', {
        output_filename: {
            'format': 'json',
            'overwrite': True,
            # 'fields': spider_cls.extracted_fields,
            'indent': 4
        }
    })

    process = CrawlerProcess(settings)
    process.crawl(spider_cls)
    process.start()


if __name__ == '__main__':

    try:
        run_spider(StubHub)

    except Exception as e:
        print("Exception occurred:", e)
