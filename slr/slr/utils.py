import datetime


def datetime2year(dt):
    """compute year fraction from datetime"""
    year_part = dt - datetime.datetime(year=dt.year, month=1, day=1)
    year_length = datetime.datetime(
        year=dt.year + 1, month=1, day=1
    ) - datetime.datetime(year=dt.year, month=1, day=1)
    return dt.year + year_part / year_length
