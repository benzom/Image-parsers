import logging

from parsers.eldorado_client import EldoradoClient
from parsers.technopark_client import TechnoparkClient, logger

if __name__ == "__main__":

    for page in range(1, 17):
        logger.info(f"PAGE {page}")
        url = f"https://www.technopark.ru/smartfony/?p={page}"
        parser = TechnoparkClient(
            market="Технопарк", url=url, img_folder="./Технопарк_телефоны/"
        )
        parser.run()

    for page in range(1, 24):
        logger.info(f"PAGE {page}")
        url = f"https://www.eldorado.ru/c/smartfony/?page={page}"
        parser = EldoradoClient(
            market="Эльдорадо", url=url, img_folder="./Эльдорадо_телефоны/"
        )
        parser.run()
