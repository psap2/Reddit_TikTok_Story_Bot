import requests
import random
from bs4 import BeautifulSoup as bs
import traceback

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    # scrapping free proxies
    soup = bs(requests.get(url).content, 'html.parser')
    # storing proxies
    proxies = []
    for row in soup.find("table", attrs={"class": "table-striped"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append(str(ip) + ":" + str(port))
        except IndexError:
            continue

    return proxies








