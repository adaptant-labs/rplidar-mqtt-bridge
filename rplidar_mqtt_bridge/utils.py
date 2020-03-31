import time
import datetime


def iso8601_timestamp():
    timestamp = int(round(time.time() * 1000))
    return datetime.datetime.utcfromtimestamp(timestamp/1000).isoformat()
