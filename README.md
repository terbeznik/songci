
<p align="center"> 
    <img src="https://github.com/terbeznik/songci/blob/master/bin/logo.png">
</p>

#  songci

## Description
`songci` is a CLI that allows you to check proxy server on a forensic way. The results of a proxy check are very detailed and extensive. A simple and powerful python API makes it easy to implement it in your project.
> Song Ci was a Chinese physician, judge, forensic medical scientist, anthropologist, and writer of the Southern Song dynasty. He was the first known anthropologist who wrote a groundbreaking book titled Collected Cases of Injustice Rectified.

## Install
```console
$ pip install songci
```

## CLI
### Single proxy

```console
$ songci -p 103.60.137.2:41630
103.60.137.2:41630 http=failed https=elite
```

### Multiple proxies

```console
$ songci -p 118.174.220.133:50616 185.18.64.106:53281 180.254.90.87:8080
180.254.90.87:8080 http=transparent https=elite evil
118.174.220.133:50616 http=elite https=failed
185.18.64.106:53281 http=failed https=failed
```

### Random proxies
Use the built-in web scraper to get and check random proxies from the internet.

```console
$ songci -r 10
118.99.93.6:8080 http=failed https=elite
103.242.13.69:8082 http=elite https=failed
103.36.35.135:8080 http=transparent https=elite
125.26.41.220:4145 http=failed https=failed
203.78.144.218:37190 http=failed https=elite
62.201.230.37:48958 http=elite https=failed
186.219.210.209:35215 http=failed https=failed
37.32.36.29:1080 http=failed https=failed
111.77.20.118:9000 http=failed https=failed
181.143.223.139:4145 http=failed https=failed
```

### Output
To write the complete check results use `-o`.

```console
$ songci -r 3 -o
180.254.90.87:8080 http=transparent https=elite evil
185.18.64.106:53281 http=elite https=elite
118.174.220.133:50616 http=failed https=failed
```

Each check contains a json with **complete results** and a HTML file of each **content manipulation** found.

```
2019-10-19T10_34_30/
|--- 180.254.90.87:8080 (http).html
|--- summary.json
```

Structure of results inside `summary.json`

```json
{
  "ip": "",
  "port": "",
  "check_headers": "",
  "check_html": "",
  "begin": "",
  "end": ""
}
```

### Additional parameters
#### Threads
`songci` uses threading to check multiple proxies at the same time. With `-t` you can set amount of threads.

```console
$ sonci -r 100 -t 10
```

### Timeout
Each check contains multiple HTTP-Requests. Default timeout for each request is 60 seconds. You can change it with `--timeout`.

```
$ songci -r 100 --timeout 20
```

## Python

### Single proxy

```pycon
>>> import songci
>>> proxy = songci.get_proxy()
>>> result = songci.check(proxy)
171.6.73.253:8080 http=anonymous https=elite
>>> result
{'ip': '171.6.73.253', 'port': '8080', 'check_headers': {'http': {'status_code': 200, 'status_code_on_proxy': None, 'client_request_headers': {'User-Agent': 'python-requests/2.20.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}, 'server_request_headers': {'args': {}, 'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip', 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6', 'Cache-Control': 'max-age=0', 'Host': 'httpbin.org', 'If-Modified-Since': 'Sat, 19 Oct 2019 11:04:22 GMT', 'User-Agent': 'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)', 'X-Proxy-Id': '438871588'}, 'origin': '183.89.1.147, 183.89.1.147', 'url': 'https://httpbin.org/get'}, 'anonymity_level': 2, 'response_headers': {'Content-Length': '527', 'Content-Type': 'application/json', 'Server': 'nginx', 'Last-Modified': 'Sat, 19 Oct 2019 11:05:20 GMT', 'Date': 'Sat, 19 Oct 2019 11:23:07 GMT'}, 'error': None}, 'https': {'status_code': 200, 'status_code_on_proxy': None, 'client_request_headers': {'User-Agent': 'python-requests/2.20.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}, 'server_request_headers': {'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.20.0'}, 'origin': '171.6.73.253, 171.6.73.253', 'url': 'https://httpbin.org/get'}, 'anonymity_level': 3, 'response_headers': {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': '*', 'Content-Encoding': 'gzip', 'Content-Type': 'application/json', 'Date': 'Sat, 19 Oct 2019 12:12:57 GMT', 'Referrer-Policy': 'no-referrer-when-downgrade', 'Server': 'nginx', 'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY', 'X-XSS-Protection': '1; mode=block', 'Content-Length': '182', 'Connection': 'keep-alive'}, 'error': None}}, 'check_html': {'http': {'status_code': 200, 'status_code_on_proxy': None, 'client_request_headers': {'User-Agent': 'python-requests/2.20.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}, 'response_headers': {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': '*', 'Content-Type': 'text/html; charset=utf-8', 'Date': 'Sat, 19 Oct 2019 12:13:07 GMT', 'Referrer-Policy': 'no-referrer-when-downgrade', 'Server': 'nginx', 'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY', 'X-XSS-Protection': '1; mode=block', 'Content-Length': '3741', 'Age': '0'}, 'content_manipulation': None, 'error': None}, 'https': {'status_code': 200, 'status_code_on_proxy': None, 'client_request_headers': {'User-Agent': 'python-requests/2.20.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}, 'response_headers': {'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Origin': '*', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html; charset=utf-8', 'Date': 'Sat, 19 Oct 2019 12:13:07 GMT', 'Referrer-Policy': 'no-referrer-when-downgrade', 'Server': 'nginx', 'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY', 'X-XSS-Protection': '1; mode=block', 'Content-Length': '1936', 'Connection': 'keep-alive'}, 'content_manipulation': None, 'error': None}}, 'begin': '2019-10-19T12_12_42', 'end': '2019-10-19T12_13_08'}
```

### Multiple proxies

```pycon
>>> proxies = songci.get_proxies(n=100)
>>> results = songci.check(proxies)
>>> type(results)
<class 'list'>
```

### Default parameters

```python
songci.check(threads=4, timeout=60)
```
