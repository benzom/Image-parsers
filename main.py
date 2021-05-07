import logging

from parsers.citilink_client import CitilinkClient
from parsers.eldorado_client import EldoradoClient
from parsers.mts_client import MTSClient
from parsers.sbermegamarket_client import SberMegaMarketClient
from parsers.technopark_client import TechnoparkClient, logger

if __name__ == "__main__":

    # for page in range(1, 17):
    #     logger.info(f"PAGE {page}")
    #     url = f"https://www.technopark.ru/smartfony/?p={page}"
    #     parser = TechnoparkClient(
    #         market="Технопарк", url=url, img_folder="./Технопарк_телефоны/"
    #     )
    #     parser.run()

    # for page in range(1, 24):
    #     logger.info(f"PAGE {page}")
    #     url = f"https://www.eldorado.ru/c/smartfony/?page={page}"
    #     parser = EldoradoClient(
    #         market="Эльдорадо", url=url, img_folder="./Эльдорадо_телефоны/"
    #     )
    #     parser.run()

    
    # for page in range(1, 12):
    #     logger.info(f"PAGE {page}")
    #     url = f"https://www.citilink.ru/catalog/smartfony/?p={page}"
    #     parser = CitilinkClient(
    #         market="Ситилинк", url=url, img_folder="./Ситилинк_телефоны/"
    #     )
    #     parser.run()

    # for page in range(1, 20):
    #     logger.info(f"PAGE {page}")
    #     url = f"https://sbermegamarket.ru/catalog/smartfony/page-{page}/"
    #     parser = SberMegaMarketClient(
    #         market="СберМегаМаркет", url=url, img_folder="./СберМегаМаркет_телефоны/"
    #     )
    #     parser.run()

    for page in range(1, 19):
    # for page in range(1, 2):
        logger.info(f"PAGE {page}")
        url = f"https://shop.mts.ru/catalog/smartfony/{page}/"
        parser = MTSClient(
            market="МТС", url=url, img_folder="./МТС_телефоны/"
        )
        parser.run()
