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


class Client:
    def __init__(self, market: str, url: str, img_folder: str):
        self.market = market
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

    def save_image(self, link, filename):
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True

            if os.path.exists(filename):
                # logger.debug(filename)
                filename = (
                    "."
                    + filename.split(".")[1]
                    + "_{0}.{1}".format(int(time.time()), filename.split(".")[-1])
                )
                # logger.debug(filename)
            with open(filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
            logger.debug("Image dowloaded")
            return filename
        else:
            logger.debug("Image Couldn't be retreived")
            return

    def save_results(self):
        file_name = "".join(self.url.split(".")[1:])
        file_name = "./data/" + re.sub(r"[^a-zA-Z0-9]", "", file_name) + ".csv"

        with open(file_name, "w") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADER)
            for item in self.result:
                writer.writerow(item)
