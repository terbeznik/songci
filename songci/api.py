import requests
import socket
import hashlib

from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
from tqdm import tqdm

from . import helper
from .__version__ import __title__, __version__

TIMEOUT = 60


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

    def __init__(self,
                 proxy,
                 reference_html=None,
                 reference_ip=None,
                 timeout=TIMEOUT):

        self.timeout = timeout

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

        self.raw = {}
        self.result = None

    def __str__(self):
        rows = [
            f"{self.result['ip']}:{self.result['port']}",
            f"http={self.result['http']}",
            f"https={self.result['https']}",
            f"content_manipulation={bool(self.result['content_manipulation'])}"
        ]
        return " ".join(rows)

    def create_result(self):
        self.result = {}
        self.result["ip"] = self.ip
        self.result["port"] = self.port
        self.result["http"] = self.raw["check_headers"]["http"]["anonymity_level"]
        self.result["https"] = self.raw["check_headers"]["https"]["anonymity_level"]
        if self.raw["check_html"]:
            self.result["content_manipulation"] = self.raw["check_html"]["content_manipulation"]
        else:
            self.result["content_manipulation"] = None

    def anonymity_level(headers, reference_ip):
        if reference_ip in str(headers):
            return "transparent"

        for header in headers["headers"]:
            if header in Check.L4_HEADER or header.lower()[:2] == "x-":
                return "anonymous"

        return "elite"

    def run(self):
        self.begin = helper.get_timestamp()

        self.check_headers()
        self.check_html()

        self.end = helper.get_timestamp()

        self.raw["begin"] = self.begin
        self.raw["end"] = self.end

        self.create_result()

    def check_headers(self):
        self.raw["check_headers"] = {}

        if not self.reference_ip:
            self.reference_ip = Check.get_reference_ip()

        for protocol in Check.PROTOCOLS:
            result = {
                "status_code": None,
                "status_code_on_proxy": None,
                "client_request_headers": None,
                "server_request_headers": None,
                "anonymity_level": None,
                "response_headers": None,
                "error": None
            }

            self.session.proxies = {protocol: f"{protocol}://{self.proxy}"}
            url = f"{protocol}://{Check.HEADERS_URL}"

            try:
                r = self.session.get(url, timeout=self.timeout)
                result["status_code"] = r.status_code
                if r.text == Check.BAD_REQUEST_400:
                    result["status_code_on_proxy"] = 400
                result["client_request_headers"] = dict(r.request.headers)
                result["server_request_headers"] = r.json()
                result["anonymity_level"] = Check.anonymity_level(
                    result["server_request_headers"],
                    self.reference_ip
                )
                result["response_headers"] = dict(r.headers)

            except Exception as e:
                result["error"] = str(type(e))

            self.raw["check_headers"][protocol] = result

    def check_html(self):
        self.raw["check_html"] = None

        if self.raw["check_headers"]["http"]["anonymity_level"]:
            self.reference_html_hash = hashlib.md5(self.reference_html).digest()

            result = {
                "status_code": None,
                "status_code_on_proxy": None,
                "client_request_headers": None,
                "response_headers": None,
                "content_manipulation": None,
                "error": None
            }

            self.session.proxies = {"http": f"http://{self.proxy}"}
            url = f"http://{Check.HTML_URL}"

            try:
                r = self.session.get(url, timeout=self.timeout)
                result["status_code"] = r.status_code
                result["client_request_headers"] = dict(r.request.headers)
                result["response_headers"] = dict(r.headers)
                if r.status_code == 200:
                    html_hash = hashlib.md5(r.content).digest()
                    if html_hash != self.reference_html_hash:
                        if r.text == Check.BAD_REQUEST_400:
                            result["status_code_on_proxy"] == 400
                        else:
                            result["content_manipulation"] = r.text
            except Exception as e:
                result["error"] = str(type(e))

            self.raw["check_html"] = result


def check(proxies, timeout=TIMEOUT):
    begin = helper.get_timestamp()
    max_threads = cpu_count()*10
    if max_threads > len(proxies):
        threads = len(proxies)
    else:
        threads = max_threads

    reference_html = get_reference_html()
    reference_ip = get_reference_ip()
    amount = len(proxies)

    welcome = f"{__title__} {__version__} | {amount} proxies | {threads} threads"
    print(welcome)

    def worker(proxy):
        c = Check(proxy,
                  reference_html=reference_html,
                  reference_ip=reference_ip,
                  timeout=timeout)
        c.run()
        tqdm.write(str(c))
        return c.result

    pool = ThreadPool(threads)
    results = list(tqdm(pool.imap(worker, proxies), total=amount, desc="Checking proxies"))
    pool.close()
    pool.join()

    end = helper.get_timestamp()

    return {
        "name": f"songci_{begin}",
        "begin": begin,
        "end": end,
        "threads": threads,
        "results": results
    }
