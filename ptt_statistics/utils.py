import calendar
import datetime
import os
from collections import namedtuple

from . import constants


def create_dir_if_not_exists():
    if not os.path.isdir(constants.dir_path):
        os.mkdir(constants.dir_path)


def check_date_tuple(date_tuple):
    year, month, day = date_tuple

    if year is None:
        errmsg = "year cannot be emtpy."
        raise ValueError(errmsg)

    current_year = datetime.datetime.today().year
    if year is not None and not 1 <= year <= current_year:
        errmsg = "Invalid year range. Should be 1 ~ {}.".format(current_year)
        raise ValueError(errmsg)

    if month is not None and not 1 <= month <= 12:
        errmsg = "Invalid month range. Should be 1 ~ 12."
        raise ValueError(errmsg)

    try:
        valid_day = calendar.monthrange(year, month)[1]
    except:
        pass
    else:
        if day is not None and not 1 <= day <= valid_day:
            errmsg = "Invalid day range. Should be 1 ~ {}.".format(valid_day)
            raise ValueError(errmsg)

    return (year, month, day)


def get_format_len_of_str(s):
    return len(str(s))


def get_format_len_of_num(n):
    l = get_format_len_of_str(n)
    l += (get_format_len_of_str(n)-1)//3
    return l


def get_format_len_of_container(container, format_type):
    if format_type == 'str':
        format_lens = map(get_format_len_of_str, (e for e in container))
    if format_type == 'num':
        format_lens = map(get_format_len_of_num, (e for e in container))

    try:
        return max(format_lens)
    except:
        return 0


def get_n_ranked_data_from_dict(original_dict, n=100):
    rank = 1
    total = 0
    n_ranked_data = []
    RankedDatum = namedtuple('RankedDatum', ['rank', 'name', 'value'])
    last_value = None
    sorted_original_dict = sorted(original_dict.items(),
                                  key=lambda x: x[1],
                                  reverse=True)

    for name, value in sorted_original_dict:
        total += 1

        if last_value is None:
            last_value = value

        if last_value > value:
            last_value = value
            rank = total

        if rank > n:
            break

        n_ranked_data.append(RankedDatum(rank, name, value))

    return n_ranked_data
