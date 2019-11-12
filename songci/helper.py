import datetime


def get_timestamp():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')
