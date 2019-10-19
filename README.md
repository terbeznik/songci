# **<span style="background-color: rgb(17,5,7); color: rgb(134,1,17)">宋慈</span>** songci

## Meaning
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
180.254.90.87:8080 http=transparent https=elite evil           118.174.220.133:50616 http=elite https=failed                        185.18.64.106:53281 http=failed https=failed
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
