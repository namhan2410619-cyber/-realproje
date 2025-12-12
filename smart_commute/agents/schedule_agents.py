import datetime

def calc_wake_time(school_time, prep_min, travel_min, weather):

    extra = 0
    if "비" in weather or "눈" in weather:
        extra += 10

    total_min = prep_min + travel_min + extra
    school_dt = datetime.datetime.combine(datetime.date.today(), school_time)
    wake_dt = school_dt - datetime.timedelta(minutes=total_min)

    return wake_dt.strftime("%H:%M")
