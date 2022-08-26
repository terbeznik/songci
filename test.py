import songci
import random
import requests
import json

from bs4 import BeautifulSoup


def free_proxy_list_net():
    r = requests.get("https://free-proxy-list.net/")
    soup = BeautifulSoup(r.text, 'html.parser')
    soup = soup.select("tbody")
    soup = soup[0].find_all("td")

    proxies = []
    for i in range(0, len(soup), 8):
        ip = soup[i].text
        port = soup[i+1].text
        proxies.append(f"{ip}:{port}")

    return proxies


#proxy = random.choice(free_proxy_list_net())
proxies = random.choices(free_proxy_list_net(), k=3)

result = songci.check(proxies)
print(json.dumps(result, indent=4))