import requests
import socket
import hashlib
import time

from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
from tqdm import tqdm

from .__version__ import __title__, __version__


def get_reference_html():
        url = f"https://{Check.HTML_URL}"
        r = requests.get(url)
        return r.content


def get_reference_ip():
    url = f"https://{Check.IP_URL}"
    r = requests.get(url)
    ip = r.json()["origin"]
    ip = ip.replace(" ", "")
    if "," in ip:
        ip = ip.split(",")[0]
    return ip


class Check():

    BAD_REQUEST_400 = "HTTP/1.1 400 Bad Request\r\n\r\n"
    HTML_URL = "httpbin.org/html"
    HEADERS_URL = "httpbin.org/get"
    IP_URL = "httpbin.org/ip"
    L4_HEADER = [
        "Mt-Proxy-ID",
        "Proxy-agent",
        "Proxy-Connection",
        "Surrogate-Capability",
        "Via",
        "Xroxy-Connection"
    ],
    PROTOCOLS = ["http", "https"]
    TIMEOUT = 60

    def __init__(self,
                 proxy,
                 reference_html=None,
                 reference_ip=None):

        try:
            self.proxy = proxy.replace(" ", "")
            self.ip, self.port = proxy.split(":")
            self.port = int(self.port)
            socket.getaddrinfo(self.ip, self.port)
        except Exception:
            raise ValueError(f"'{self.proxy}' invalid proxy format")

        self.reference_html = reference_html if reference_html else get_reference_html()
        self.reference_ip = reference_ip if reference_ip else get_reference_ip()
        self.session = requests.Session()

        self.result = {
            "ip": self.ip,
            "port": self.port,
            "country": None,
            "begin": None,
            "end": None,
            "duration": None,
            "http": {
                "response_time": None,
                "level": None,
                "error": None
            },
            "https": {
                "response_time": None,
                "level": None,
                "error": None
            },
            "manipulation": {
                "html": None,
                "error": None
            }
        }

    def pprint(self):
        proxy = f"{self.ip}:{self.port}"
        http = f"{self.result['http']['level']}" if self.result["http"]["level"] else "failed"
        https = f"{self.result['https']['level']}" if self.result["https"]["level"] else "failed"
        manipulation = "true" if self.result["manipulation"]["html"] else "false"
        s = [
            proxy,
            f"http={http}",
            f"https={https}",
            f"manipulation={manipulation}"
        ]
        s = " | ".join(s)
        tqdm.write(s)

    def anonymity_level(headers, reference_ip):
        if reference_ip in str(headers):
            return "transparent"

        for header in headers["headers"]:
            if header in Check.L4_HEADER or header.lower()[:2] == "x-":
                return "anonymous"

        return "elite"

    def run(self):
        begin = time.time()

        self.check_geo()
        self.check_headers()
        self.check_manipulation()

        end = time.time()

        self.result["begin"] = begin
        self.result["end"] = end
        self.result["duration"] = round(end-begin, 1)

    def check_geo(self):
        try:
            payload = {"ip": self.ip} 
            r = requests.get("https://ip2c.org/", params=payload)
            country = r.text.split(";")[1]
            self.result["country"] = country
        except Exception:
            self.result["county"] = None

    def check_headers(self):
        if not self.reference_ip:
            self.reference_ip = Check.get_reference_ip()

        for protocol in Check.PROTOCOLS:
            self.session.proxies = {protocol: f"{protocol}://{self.proxy}"}
            url = f"{protocol}://{Check.HEADERS_URL}"

            try:
                start = time.time()
                r = self.session.get(url, timeout=Check.TIMEOUT)
                end = time.time()

                self.result[protocol]["level"] = Check.anonymity_level(r.json(), self.reference_ip)
                self.result[protocol]["response_time"] = round(end-start, 1)
            except Exception as e:
                self.result[protocol]["error"] = str(e)

    def check_manipulation(self):
        if self.result["http"]:
            self.reference_html_hash = hashlib.md5(self.reference_html).digest()

            self.session.proxies = {"http": f"http://{self.proxy}"}
            url = f"http://{Check.HTML_URL}"

            try:
                r = self.session.get(url, timeout=Check.TIMEOUT)
                if r.status_code == 200:
                    html_hash = hashlib.md5(r.content).digest()
                    if html_hash != self.reference_html_hash:
                        if r.text != Check.BAD_REQUEST_400:
                            self.result["manipulation"]["html"] = r.text
            except Exception as e:
                self.result["manipulation"]["error"] = str(e)


def check_one(proxy, verbose=False):
    c = Check(proxy)
    c.run()
    if verbose:
        c.pprint()
    return c.result


def check_many(proxies, verbose=False):
    max_threads = cpu_count()*10
    if max_threads > len(proxies):
        threads = len(proxies)
    else:
        threads = max_threads

    reference_html = get_reference_html()
    reference_ip = get_reference_ip()
    amount = len(proxies)

    def worker(proxy):
        c = Check(proxy,
                  reference_html=reference_html,
                  reference_ip=reference_ip)
        c.run()
        if verbose:
            c.pprint()
        return c.result

    pool = ThreadPool(threads)
    if verbose:
        results = list(tqdm(pool.imap(worker, proxies), total=amount, desc="Checking proxies"))
    else:
        results = list(pool.imap(worker, proxies))
    pool.close()
    pool.join()

    return results


def check(proxies, verbose=False):
    if type(proxies) == str:
        return check_one(proxies, verbose=verbose) 
    elif type(proxies) == list:
        if len(proxies) > 1:
            return check_many(proxies, verbose=verbose)
        else:
            return check_one(proxies[0], verbose=verbose)  
