import bs4
import collections
import csv
import logging
import re
import requests


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("wb")

HEADER = (
    "Item Name",
    'URL'
)

ParseResult = collections.namedtuple(
    "ParseResult",
    (
        "item_name",
        "url"
    ),
)

class Client:

    def __init__(self):
        self.url = "https://www.technopark.ru/apple-iphone/"
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36",
            "Accept-Language": "ru",
        }
        self.result = []

    
    def load_page(self):
        res = self.session.get(self.url)
        res.raise_for_status()
        return res.text


    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, features="lxml")
        container = soup.select("div.card-listing__body")
        for block in container:
            self.parse_block(block)


    def parse_block(self, block):
        #logger.info(block)
        #logger.info("-" * 100)

        url_block = block.select_one("a.card-listing__overlay-link.js-analytics-card--link")
        if not url_block:
            logger.error("no a block")
            return
        url = url_block.get("href")
        if not url:
            logger.error("no href")
            return
        item_name = block.select_one("div.card-listing__name")
        if not item_name:
            logger.error("no a block")
            return

        self.result.append(ParseResult(
            item_name=re.sub(r"[^а-яА-Яa-zA-Z0-9 ]+", "", item_name.text),
            url=self.url[:-1] + url
        ))

    
    def save_results(self):
        path = "test.csv"

        with open(path, "w") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADER)
            for item in self.result:
                writer.writerow(item)

    def run(self):
        text = self.load_page()
        self.parse_page(text)
        logger.info(f"Got {len(self.result)} items")
        self.save_results()


if __name__ == "__main__":
    parser = Client()
    parser.run()