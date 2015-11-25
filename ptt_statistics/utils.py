import calendar
import datetime
import os

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
