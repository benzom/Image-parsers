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


class TechnoparkClient(Client):
    def __init__(self, market: str, url: str, img_folder: str):
        super().__init__(market, url, img_folder)

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

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, features="lxml")
        container = soup.select("div.card-listing__body")
        price_container = soup.select("div.card-listing__aside")
        for basic_block, price_block in zip(container, price_container):
            self.parse_block(basic_block, price_block)

    def run(self):
        text = self.load_page()
        self.parse_page(text)
        logger.info(f"Got {len(self.result)} items")
        self.save_results()
