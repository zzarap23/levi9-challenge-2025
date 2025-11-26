from datetime import datetime, timedelta, date

def validate_time_format(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def validate_date(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return d >= date.today()
    except ValueError:
        return False
    
def time_to_min(time_str):
    t = datetime.strptime(time_str, "%H:%M")
    return t.hour * 60 + t.minute

def is_half_hour(time_str):
    try:
        t = datetime.strptime(time_str, "%H:%M")
        return t.minute in (0,30)
    except ValueError:
        return False


def overlaps(t1, d1, t2, d2):
    start1 = time_to_min(t1)
    end1 = start1 + d1

    start2 = time_to_min(t2)
    end2 = start2 + d2

    return not (end1 <= start2 or end2 <= start1)

def iterate_date(start_date_str, end_date_str):
    start = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    current = start

    while current <= end:
        yield current
        current += timedelta(days=1)

def min_to_time(minutes):
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"

