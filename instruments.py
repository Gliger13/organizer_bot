import re
from datetime import datetime, timedelta


is_time = re.compile(r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])$')


def get_sec_left(time_end: str) -> int:
    if not re.match(is_time, time_end):
        raise TypeError('Entering str is not time')
    hours_end, minutes_end = tuple(map(int, time_end.split(':')))
    time_start = datetime.now()
    delta_start = timedelta(hours=time_start.hour, minutes=time_start.minute, seconds=time_start.second)
    delta_end = timedelta(hours=hours_end, minutes=minutes_end)
    delta_left = delta_end - delta_start
    return delta_left.seconds


if __name__ == '__main__':
    time = '23:00'
    print(get_sec_left(time))
