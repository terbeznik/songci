import sys
import argparse

from . import api
from . import helper
from .__version__ import __version__


def main():
    proxies_help = "single proxy host:port or multiple whitespace seperated proxies"
    version_help = "current version"
    output_help = "write results songci_<TIMESTAMP>.json"
    input_help = "use proxy list file"
    timeout_help = f"set timeout per request (default: {api.TIMEOUT})"

    parser = argparse.ArgumentParser(description='songci checks proxies')
    parser.add_argument("proxies",
                        type=str,
                        nargs="*",
                        help=proxies_help)
    parser.add_argument("--version",
                        "-V",
                        action="store_true",
                        help=version_help)
    parser.add_argument("--output",
                        "-o",
                        action="store_true",
                        help=output_help)
    parser.add_argument("--input",
                        "-i",
                        type=str,
                        help=input_help)
    parser.add_argument("--timeout",
                        "-t",
                        type=int,
                        default=api.TIMEOUT,
                        help=timeout_help)
    args = parser.parse_args(sys.argv[1:])

    # VERSION
    if args.version:
        print(__version__)

    # PROXIES
    proxies = []
    if len(args.proxies) > 0:
        proxies += args.proxies
    if args.input:
        path = args.input
        proxies += helper.read(path)

    if proxies:
        # CHECK
        result = api.check(proxies, timeout=args.timeout)

        # WRITE
        if args.output:
            helper.write(result)


if __name__ == "__main__":
    main()
