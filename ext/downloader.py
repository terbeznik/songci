import requests
import sys
import random

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


def spys_me():
    r = requests.get("http://spys.me/proxy.txt")
    proxies = []
    for line in r.text.splitlines()[9:-2]:
        proxy = line.split(" ")[0]
        proxies.append(proxy)

    return proxies


def proxy_daily_com():
    r = requests.get("https://proxy-daily.com/")
    soup = BeautifulSoup(r.text, "html.parser")
    areas = soup.select(".freeProxyStyle")

    proxies = []
    for area in areas:
        proxies += area.text.splitlines()

    return proxies


def proxyscrape_com():
    r = requests.get("https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all")
    proxies = r.text.splitlines()

    return proxies


if len(sys.argv) > 1:
    n = int(sys.argv[1])
else:
    n = 1000

proxies = free_proxy_list_net()+spys_me()+proxy_daily_com()+proxyscrape_com()
random.shuffle(proxies)
proxies = proxies[:n]

with open("proxies.txt", "w") as f:
    for proxy in proxies:
        f.write(f"{proxy}\n")
