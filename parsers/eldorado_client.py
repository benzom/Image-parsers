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


class EldoradoClient(Client):
    def __init__(self, market: str, url: str, img_folder: str):
        super().__init__(market, url, img_folder)

    def parse_block(self, block):
        url_block = block.select_one("a.Ju")
        if not url_block:
            logger.error("no a block")
            return
        url = url_block.get("href")
        item_name = url_block.text
        if not url:
            logger.error("no url presented")
            return

        img_block = block.select_one("a.vu")
        if not img_block:
            logger.error("no image block")
            return
        img = img_block.select_one("img")["src"]
        if not url:
            logger.error("no img presented")
            return
        # remove resize to get better quality
        img = img[:-16]
        filename = self.img_folder + img.split("/")[-1]
        img_id = self.save_image(img, filename)

        p_block = block.select_one("span.hF.lF")
        # logger.debug(p_block)
        if not p_block:
            logger.error("no price block")
            return
        price = p_block.text
        # price = p_block.span.text
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
        container = soup.find_all("li", class_="xu")
        for block in container:
            self.parse_block(block)

    def run(self):
        text = self.load_page()
        self.parse_page(text)
        logger.info(f"Got {len(self.result)} items")
        self.save_results()
