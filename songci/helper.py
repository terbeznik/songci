import datetime
import json
import os

from . import api


def get_timestamp():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')


def read(path):
    with open(path, "r") as f:
        proxies = f.read().splitlines()
    return proxies


def write(result):
    with open(f"{result['name']}.json", "w") as f:
        json.dump(result, f, indent=4)
