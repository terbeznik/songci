
<p align="center"> 
    <img src="https://github.com/terbeznik/songci/blob/master/ext/logo.png">
</p>

#  songci

## Description
`songci` is a python module that allows you to check proxy server on a forensic way. 
The focus is on:
- anonymity level 🥇
- content manipulation detection 😈
- protocol seperated results 🗂️

The results of a proxy check are very detailed and extensive.
> Song Ci was a Chinese physician, judge, forensic medical scientist, anthropologist, and writer of the Southern Song dynasty. He was the first known anthropologist who wrote a groundbreaking book titled Collected Cases of Injustice Rectified.

## Install

```console
$ pip install songci
```

## Getting started

#### Check single proxy

```pycon
>>> import songci
>>> proxy = "45.77.254.125:3128"
>>> result = songci.check(proxy)
>>> result
{
    "ip": "45.77.254.125",
    "port": 3128,
    "country": "US",
    "begin": 1575746554.682173,
    "end": 1575746559.2740119,
    "duration": 4.6,
    "http": {
        "response_time": 0.9,
        "level": "elite",
        "error": null
    },
    "https": {
        "response_time": 2.9,
        "level": "elite",
        "error": null
    },
    "manipulation": {
        "html": null,
        "error": null
    }
}
```

#### Check multiple proxies

```pycon
>>> proxies = ["151.237.126.34:33695", "41.164.247.186:53281", "194.226.34.132:5555"]
>>> results = songci.check()
>>> results
[
    {
        "ip": "151.237.126.34",
        "port": 33695,
        "country": "BG",
        ...
```

## CLI
#### How to use

```console
$ songci --help
Usage: songci [OPTIONS] [PROXIES]...

Options:
  --version
  -i FILENAME  Input from list of proxies
  -o FILENAME  Outputfilename to write summary as json
  --help       Show this message and exit.
```

#### Check single proxy

```console
$ songci 104.167.113.48:3128
104.167.113.48:3128 | http=transparent | https=elite | manipulation=false
```

#### Check multiple proxies

```console
$ songci 95.175.14.54:8080 104.167.113.48:3128 36.92.116.26:8080 
95.175.14.54:8080 | http=None | https=elite | manipulation=false
104.167.113.48:3128 | http=transparent | https=elite | manipulation=false
36.92.116.26:8080 | http=anonymous | https=elite | manipulation=true
```

#### Use proxy list

One line one proxy `host:port` like this `proxies.txt`

```
103.79.164.70:53281
190.152.36.102:31884
31.40.136.209:53281
80.90.133.250:8080
183.88.16.33:8080
...
```

```console
$ songci -i proxies.txt
103.79.164.70:53281 | http=transparent | https=elite | manipulation=false
190.152.36.102:31884 | http=elite | https=elite | manipulation=false
31.40.136.209:53281 | http=elite | https=elite | manipulation=false
80.90.133.250:8080 | http=transparent | https=elite | manipulation=false
183.88.16.33:8080 | http=anonymous | https=elite | manipulation=false 
...
```

#### Save results to file

Use `-o` flag to save results in a JSON-File

```console
$ songci 151.237.126.34:33695 95.175.14.54:8080 104.167.113.48:3128 -o summary.json
```

Example output file `summary.json`

```json
[
    {
        "ip": "151.237.126.34",
        "port": 33695,
        "country": "BG",
        ...
```




