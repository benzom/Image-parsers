import logging

from parsers.technopark_client import TechnoparkClient, logger

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("wb")

if __name__ == "__main__":

    for page in range(1, 2):
        logger.info(f"PAGE {page}")
        url = "https://www.technopark.ru/smartfony/?p=" + str(page)
        parser = TechnoparkClient(
            market="Технопарк", url=url, img_folder="./Технопарк_телефоны/"
        )
        parser.run()
