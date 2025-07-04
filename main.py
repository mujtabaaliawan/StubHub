from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from stubhub.spiders.stubhub_spider import StubHub


def run_spider(spider_cls):
    settings = get_project_settings().copy()
    output_filename = f"{spider_cls.name}_results.json"
    log_filename = f"{spider_cls.name}_log.txt"
    settings.set('LOG_LEVEL', 'INFO')  # Or 'DEBUG' or 'ERROR' if needed
    settings.set('LOG_FILE', log_filename)

    settings.set('FEEDS', {
        output_filename: {
            'format': 'json',
            'overwrite': True,
            'indent': 4
        }
    })

    process = CrawlerProcess(settings)
    print("Starting running scraper")
    process.crawl(spider_cls)
    print(f"Scraping completed. Check results in {output_filename} and log in {log_filename}")
    process.start()


if __name__ == '__main__':

    try:
        run_spider(StubHub)

    except Exception as e:
        print("Exception occurred:", e)
