import requests
import socket
import hashlib
import json

from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm
from colorama import init as init_colorama
from colorama import Fore, Back, Style

from . import helper

THREADS = 4
TIMEOUT = 60
PROTOCOLS = ["http", "https"]

init_colorama()
ANONYMITY_LEVEL_OUTPUT = {
    1: f"{Style.BRIGHT}transparent{Style.RESET_ALL}",
    2: f"{Style.BRIGHT}{Fore.CYAN}anonymous{Style.RESET_ALL}",
    3: f"{Style.BRIGHT}{Fore.GREEN}elite{Style.RESET_ALL}",
    None: f"{Style.BRIGHT}{Fore.RED}failed{Style.RESET_ALL}"
}
CONTENT_MANIPULATION_OUTPUT = f"{Style.BRIGHT}{Back.RED}manipulation{Style.RESET_ALL}"


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
    ]

    def __init__(self,
                 proxy,
                 reference_html=None,
                 reference_ip=None,
                 protocols=PROTOCOLS,
                 timeout=TIMEOUT):

        self.protocols = protocols
        self.timeout = timeout

        try:
            self.proxy = proxy.replace(" ", "")
            self.ip, self.port = proxy.split(":")
            socket.getaddrinfo(self.ip, self.port)
        except Exception as e:
            raise e

        self.reference_html = reference_html
        self.reference_ip = reference_ip
        self.session = requests.Session()

        self.result = {
            "ip": self.ip,
            "port": self.port,
        }

    def __str__(self):
        return json.dumps(self.result, indent=4)

    @property
    def result_for_humans(self):
        country = f"{Style.DIM}{Fore.CYAN}{self.result['country_name']}{Style.RESET_ALL}" if self.result["country_name"] else ""
        http = ANONYMITY_LEVEL_OUTPUT[self.result["check_headers"]["http"]["anonymity_level"]]
        https = ANONYMITY_LEVEL_OUTPUT[self.result["check_headers"]["https"]["anonymity_level"]]

        if self.result["check_html"]["http"]["content_manipulation"] or self.result["check_html"]["https"]["content_manipulation"]:
            content_manipulation = CONTENT_MANIPULATION_OUTPUT
        else:
            content_manipulation = ""

        cols = [
            f"{self.ip}:{self.port}",
            country,
            f"http={http}",
            f"https={https}",
            content_manipulation
        ]

        return f" ".join(cols)

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

    def anonymity_level(headers, reference_ip):
        if reference_ip in str(headers):
            return 1

        for header in headers["headers"]:
            if header in Check.L4_HEADER or header.lower()[:2] == "x-":
                return 2

        return 3

    def run(self):
        self.begin = helper.get_timestamp()

        self.check_country()
        self.check_headers()
        self.check_html()

        self.end = helper.get_timestamp()

        self.result["begin"] = self.begin
        self.result["end"] = self.end

    def check_country(self):
        result = helper.get_country(self.ip)
        self.result.update(result)

    def check_headers(self):
        self.result["check_headers"] = {}

        if not self.reference_ip:
            self.reference_ip = Check.get_reference_ip()

        for protocol in self.protocols:
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

            self.result["check_headers"][protocol] = result

    def check_html(self):
        self.result["check_html"] = {}

        if not self.reference_html:
            self.reference_html = Check.get_reference_html()

        self.reference_html_hash = hashlib.md5(self.reference_html).digest()

        for protocol in self.protocols:
            result = {
                "status_code": None,
                "status_code_on_proxy": None,
                "client_request_headers": None,
                "response_headers": None,
                "content_manipulation": None,
                "error": None
            }

            self.session.proxies = {protocol: f"{protocol}://{self.proxy}"}
            url = f"{protocol}://{Check.HTML_URL}"

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

            self.result["check_html"][protocol] = result


def check(proxy_data, threads=THREADS, timeout=TIMEOUT):
    if isinstance(proxy_data, str):
        proxies = [proxy_data]
    elif isinstance(proxy_data, list):
        proxies = proxy_data

    if len(proxies) > 1:
        threads = threads if len(proxies) > threads else len(proxies)
        reference_html = Check.get_reference_html()
        reference_ip = Check.get_reference_ip()

        def worker(proxy):
            c = Check(proxy,
                      reference_html=reference_html,
                      reference_ip=reference_ip,
                      timeout=timeout)
            c.run()
            tqdm.write(c.result_for_humans)
            return c.result

        pool = ThreadPool(threads)
        amount = len(proxy_data)
        results = list(tqdm(pool.imap(worker, proxy_data), total=amount, desc="Checking proxies"))
        pool.close()
        pool.join()
        return results
    elif len(proxies) == 1:
        proxy = proxies[0]
        c = Check(proxy, timeout=timeout)
        c.run()
        print(c.result_for_humans)
        return c.result
