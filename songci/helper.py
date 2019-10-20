import requests
import random
import datetime
import json
import os
import ipaddress

from bs4 import BeautifulSoup

from . import api
from . import data


def get_country(ip):
    ip = ipaddress.ip_address(ip)
    result = {
        "country_code": None,
        "country_name": None
    }
    for r in data.RANGES:
        ip_from = ipaddress.ip_address(r["ip_from"])
        ip_to = ipaddress.ip_address(r["ip_to"])
        if ip_from < ip < ip_to:
            result["country_code"] = r["country_code"]
            result["country_name"] = r["country_name"]
            return result
    return result


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
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')


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
                            html_path = f"{name}/{result['ip']}_{result['port']}_{protocol}.html"
                            with open(html_path, "w") as f:
                                f.write(html)
                    except Exception as e:
                        print(e)
        else:
            summary_path = f"./{name}.json"

        with open(summary_path, "w") as f:
            json.dump(data, f, indent=4)
    elif isinstance(data, dict):
        name = data["end"]
        summary_path = f"./{name}_{data['ip']}_{data['port']}.json"
        with open(summary_path, "w") as f:
            json.dump(data, f)
