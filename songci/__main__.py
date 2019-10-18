import json
import sys
import argparse

from . import api
from . import helper


def main():
    parser = argparse.ArgumentParser(description='songci checks proxies')
    parser.add_argument("--proxies", type=str, nargs="+")
    parser.add_argument("--threads", type=int, default=api.THREADS)
    parser.add_argument("--timeout", type=int, default=api.TIMEOUT)
    parser.add_argument("--random", type=int)
    parser.add_argument("--output", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(sys.argv[1:])

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

        # VERBOSE
        if args.verbose:
            if isinstance(result_data, list):
                for result in result_data:
                    print("-"*50)
                    s = json.dumps(result, indent=4)
                    print(s)
                    print("-"*50)
            elif isinstance(result_data, dict):
                s = json.dumps(result_data, indent=4)
                print(s)

        # OUTPUT
        if args.output:
            helper.write(result_data)


if __name__ == "__main__":
    main()
