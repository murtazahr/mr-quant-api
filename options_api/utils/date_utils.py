from datetime import datetime

QUANTSBIN_FORMAT = '%Y%m%d'


def current_dt_as_string(str_format: str):
    return dt_as_string(datetime.now(), str_format)


def dt_as_string(date: datetime, str_format: str):
    return date.strftime(str_format)
