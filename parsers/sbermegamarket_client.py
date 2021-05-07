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


class SberMegaMarketClient(Client):
    def __init__(self, market: str, url: str, img_folder: str):
        super().__init__(market, url, img_folder)

    def parse_block(self, block):
        url_block = block.select_one("a")
        if not url_block:
            logger.error("no a block")
            return
        url = url_block.get("href")
        if not url:
            logger.error("no url presented")
            return

        name_block = block.select_one("header.card-prod--title")
        if not url_block:
            logger.error("no a block")
            return
        item_name = name_block.select_one("a").get("title")
        if not url:
            logger.error("no name presented")
            return

        img_block = block.select_one("div.card-prod--photos.no-active")
        if not img_block:
            logger.error("no image block")
            return
        # logger.debug(img_block)
        img = img_block.select_one("img")["src"]
        if not url:
            logger.error("no img presented")
            return
        # logger.debug(img)
        filename = self.img_folder + img.split("/")[-1]
        img_id = self.save_image(img, filename)

        price_block = block.select_one("div.current.favoritePrice")
        # logger.debug(price_block)
        if not price_block:
            logger.error("no price block")
            return
        price = price_block.text
        logger.debug(price)
        if not price:
            logger.error("no price presented")
            return

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
        container = soup.find_all("article", class_="card-prod card-prod-grid")
        for block in container:
            self.parse_block(block)

    def run(self):
        text = self.load_page()
        self.parse_page(text)
        logger.info(f"Got {len(self.result)} items")
        self.save_results()
