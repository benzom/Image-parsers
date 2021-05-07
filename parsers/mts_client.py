import bs4
import collections
import logging
import re
import requests

from parsers.client import Client, logger

ParseResult = collections.namedtuple(
    "ParseResult",
    ("market", "item_name", "img_id", "price", "url"),
)


class MTSClient(Client):
    def __init__(self, market: str, url: str, img_folder: str):
        super().__init__(market, url, img_folder)

    def parse_block(self, block):
        url_block = block.select_one("a.card-product-description__img-link")
        if not url_block:
            logger.error("no a block")
            return
        url = url_block.get("href")
        item_name = url_block.get("aria-label")
        if not url:
            logger.error("no url presented")
            return
        item_name = re.sub("\u20bd", "", item_name)
        item_name = re.sub("\s", "", item_name)

        img_block = block.select_one("img.gallery__img")
        if not img_block:
            logger.error("no image block")
            return
        # logger.debug(img_block)
        img = img_block["data-src"]
        if not url:
            logger.error("no img presented")
            return
        # logger.debug(img)
        filename = self.img_folder + img.split("/")[-1]
        # logger.debug(img)
        # logger.debug(filename)
        img_id = self.save_image(img, filename)

        price_block = block.select_one("div.hidden-price")
        # logger.debug(price_block)
        if not price_block:
            logger.error("no price block")
            return
        price = price_block.text
        # logger.debug(price)
        if not price:
            logger.error("no price presented")
            return
        price = re.sub("\u20bd", "", price)
        price = re.sub("\s", "", price)

        self.result.append(
            ParseResult(
                market=self.market,
                item_name=item_name,
                img_id=img_id,
                price=price,
                url=url,
            )
        )

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, features="lxml")
        container = soup.find_all("div", class_="card-product-wrapper card-product-wrapper--catalog")
        for block in container:
            self.parse_block(block)

    def run(self):
        text = self.load_page()
        self.parse_page(text)
        logger.info(f"Got {len(self.result)} items")
        self.save_results()
