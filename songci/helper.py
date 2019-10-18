import requests
import random
import datetime
import json
import os

from bs4 import BeautifulSoup

from . import api


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


def get_proxies(n=10):
    proxies = list(set(free_proxy_list_net()+spys_me()+proxy_daily_com()+proxyscrape_com()))
    random.shuffle(proxies)
    return proxies[:n]


def get_proxy():
    proxies = get_proxies()
    return proxies[0]


def get_timestamp():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S')


def write(data, content_manipilation_as_html=True):
    if isinstance(data, list):
        name = get_timestamp()

        if content_manipilation_as_html:
            if not os.path.exists(name):
                os.makedirs(name)
            summary_path = f"./{name}/summary.json"

            for result in data:
                for protocol in api.PROTOCOLS:
                    try:
                        html = result["check_html"][protocol]["content_manipulation"]
                        if html:
                            html_path = f"{name}/{result['ip']}:{result['port']} ({protocol}).html"
                            with open(html_path, "w") as f:
                                f.write(html)
                    except Exception as e:
                        print(e)
        else:
            summary_path = f"./{name}.json"

        with open(summary_path, "w") as f:
            json.dump(data, f, indent=4)
    elif isinstance(data, dict):
        summary_path = f"./{name}_{data['ip']}:{data['port']}.json"

