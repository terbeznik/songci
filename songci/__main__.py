import json
import sys
import argparse

from . import api
from . import helper


def main():
    parser = argparse.ArgumentParser(description='songci checks proxies')
    parser.add_argument("--proxies", "-p", type=str, nargs="+")
    parser.add_argument("--threads", type=int, default=api.THREADS)
    parser.add_argument("--timeout", type=int, default=api.TIMEOUT)
    parser.add_argument("--random", "-r", type=int)
    parser.add_argument("--output", "-o", action="store_true")
    parser.add_argument("--version", "-V", action="store_true")
    args = parser.parse_args(sys.argv[1:])

    # VERSION
    if args.version:
        print("0.0.6")

    # PROXIES
    proxy_data = []
    if args.proxies:
        proxy_data += args.proxies
    if args.random:
        proxy_data += helper.get_proxies(n=args.random)
    if len(proxy_data) == 1:
        proxy_data = proxy_data[0]

    if proxy_data:
        # CHECK
        result_data = api.check(proxy_data,
                                timeout=args.timeout,
                                threads=args.threads)

        # OUTPUT
        if args.output:
            helper.write(result_data)


if __name__ == "__main__":
    main()
