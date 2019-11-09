
<p align="center"> 
    <img src="https://github.com/terbeznik/songci/blob/master/ext/logo.png">
</p>

#  songci

## Description
`songci` is a CLI that allows you to check proxy server on a forensic way. 
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

## How to use

```console
$ songci --help
Usage: songci [OPTIONS] [PROXIES]...

Options:
  --version
  -i FILENAME  Input from list of proxies
  -o FILENAME  Outputfilename to write summary as json
  --help       Show this message and exit.
```

## Examples

### Check single proxy

```console
$ songci 104.167.113.48:3128
104.167.113.48:3128 http=transparent https=elite content_manipulation=False
```

### Check multiple proxies

```console
$ songci 95.175.14.54:8080 104.167.113.48:3128 36.92.116.26:8080 
95.175.14.54:8080 http=None https=elite content_manipulation=False
104.167.113.48:3128 http=transparent https=elite content_manipulation=False
36.92.116.26:8080 http=anonymous https=elite content_manipulation=True
```

### Use proxy list

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
103.79.164.70:53281 http=transparent https=elite content_manipulation=False
190.152.36.102:31884 http=elite https=elite content_manipulation=False
31.40.136.209:53281 http=elite https=elite content_manipulation=False
80.90.133.250:8080 http=transparent https=elite content_manipulation=False
183.88.16.33:8080 http=anonymous https=elite content_manipulation=False 
...
```

### Save results to file

Use `-o` flag to save results in a JSON-File

```console
$ songci 95.175.14.54:8080 104.167.113.48:3128 -o summary.json
```

Example output file `summary.json`

```json
{
    "begin": "2019-10-20T19-35-41",
    "end": "2019-10-20T19-36-24",
    "threads": 2,
    "results": [
        {
            "ip": "95.175.14.54",
            "port": 8080,
            "http": "transparent",
            "https": "elite",
            "content_manipulation": null
        },
        {
            "ip": "104.167.113.48",
            "port": 3128,
            "http": "transparent",
            "https": "elite",
            "content_manipulation": null
        }
    ]
}
```




