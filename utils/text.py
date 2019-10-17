from utils.util import get_full_path
import os
from random import randrange
import datetime


def parse_int_to_thousands_k(number: int):
    if number < 1000:
        return number
    before_dot = number // 1000
    after_dot = ''
    remainder_hundreds = number % 1000
    if remainder_hundreds != 0:
        after_dot = '.' + str(remainder_hundreds // 100)
    return f'{before_dot}{after_dot}k'


def limit_string_length(name: str, limit: int) -> str:
    if len(name) > limit:
        return name[:limit]
    return name


def convert_seconds_to_human_friendly(seconds: int):
    result = ''
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    if minutes >= 1:
        result += f'{minutes} minutes and'
    return f'{result} {remaining_seconds} seconds'


def format_unix_to_time(unix_time, format_time='%Y-%m-%d'):
    return datetime.datetime.utcfromtimestamp(unix_time).strftime(format_time)


def get_random_fact():
    text_path = get_full_path('texts', 'random_facts.csv')
    filesize = os.path.getsize(text_path)
    offset = randrange(filesize)

    with open(text_path, 'r') as f:
        f.seek(offset)
        f.readline()
        return f.readline()

