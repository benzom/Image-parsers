import bs4
import requests

session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36",
    "Accept-Language": "ru",
}

res = session.get("https://www.eldorado.ru/c/smartfony/")
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, features="lxml")
container = soup.find_all("li", class_="xu")
print(len(container))
print("-" * 100)
# print("-" * 100)
