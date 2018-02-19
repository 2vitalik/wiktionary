from datetime import datetime, timedelta


PLUS_HOURS = 2  # info: difference with server time

formats = {
    'dt': '%Y-%m-%d %H:%M:%S',
    'dts': '%Y-%m-%d__%H-%M-%S',  # info: datetime slug
    'Ymd': '%Y-%m-%d',
    '[hms]': '[%H:%M:%S]',
    'Ym': '%Y-%m',
    'dh': '%dd-%Hh',
}


def t():  # info: short function to return time
    return datetime.now().strftime("[%H:%M:%S]")


def dt(value=None, utc=False):
    return dtf('dt', value, utc)


def dtf(fmt, value=None, utc=False):  # info: datetime format
    value = value or datetime.now()
    # if not utc:
    #     value += timedelta(hours=PLUS_HOURS)
    return value.strftime(formats[fmt])


def dtp(value, fmt='dt'):  # info: datetime parse
    return datetime.strptime(value, formats[fmt])
