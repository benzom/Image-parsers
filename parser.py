import bs4
import collections
import csv
import logging
import os
import re
import requests
import shutil
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wb")

HEADER = ("market", "item_name", "img_id", "price", "url")

ParseResult = collections.namedtuple(
    "ParseResult",
    ("market", "item_name", "img_id", "price", "url"),
)


class Client:
    def __init__(self, url: str, img_folder: str):
        self.market = "Технопарк"
        self.url = url
        self.img_folder = img_folder
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
        price_container = soup.select("div.card-listing__aside")
        for basic_block, price_block in zip(container, price_container):
            self.parse_block(basic_block, price_block)

    def save_image(self, link):
        filename = self.img_folder + link.split("/")[-1]
        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(link, stream=True)
        # Check if the image was retrieved successfully
        if r.status_code == 200:
            r.raw.decode_content = True

            if os.path.exists(filename):
                filename = (
                    "." + filename.split(".")[1] + "_{}.jpg".format(int(time.time()))
                )
            with open(filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
            logger.debug("Image dowloaded")
            return filename
        else:
            logger.debug("Image Couldn't be retreived")
            return

    def parse_block(self, block, price_block):
        url_block = block.select_one(
            "a.card-listing__overlay-link.js-analytics-card--link"
        )
        if not url_block:
            logger.error("no a block")
            return
        url = url_block.get("href")
        if not url:
            logger.error("no url presented")
            return

        img_block = block.select_one("img")
        if not img_block:
            logger.error("no image block")
            return
        img = img_block["data-src"]
        if not url:
            logger.error("no img presented")
            return
        img_id = self.save_image(img)

        item_name = block.select_one("div.card-listing__name")
        if not item_name:
            logger.error("no item name data")
            return

        # listing__price
        p_block = price_block.select_one("div.card-listing__price")
        if not p_block:
            logger.error("no price block")
            return
        price = p_block.span.text
        if not price:
            logger.error("no price presented")
            return
        price = re.sub("\u20bd", "", price)
        price = re.sub("\s", "", price)

        self.result.append(
            ParseResult(
                market=self.market,
                item_name=re.sub(r"[^а-яА-Яa-zA-Z0-9 ]+", "", item_name.text),
                img_id=img_id,
                price=price,
                url=self.url[:-1] + url,
            )
        )

    def save_results(self):
        file_name = "".join(self.url.split(".")[1:])
        file_name = re.sub(r"[^a-zA-Z0-9]", "", file_name) + ".csv"

        with open(file_name, "w") as f:
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

    for page in range(1, 7):
        logger.info(f"PAGE {page}")
        url = "https://www.technopark.ru/apple-iphone/?p=" + str(page)
        parser = Client(url=url, img_folder="./Технопарк/")
        parser.run()
