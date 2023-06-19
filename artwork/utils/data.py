import time
from datetime import datetime as dt
from datetime import timedelta as td
from artwork.db.mongo import db


def get_week_days(year, week):
    startdate = dt.fromisocalendar(year, week, 1)

    days = []
    for i in range(7):
        day = startdate + td(days=i)
        days.append(day)
    
    return days


def add_campaign(
        year,
        week,
        topic,
        names,
        width,
        height,
        prompt_essay,
        prompt_artwork
):
    days = get_week_days(year, week)

    d = {
        "date": days[0],
        "topic": topic,
        "width": width,
        "height": height,   
        "data": {days[i].strftime("%Y%m%d"): name for i, name in enumerate(names)},
        "prompt": {
            "essay": prompt_essay,
            "artwork": prompt_artwork
        }
    }

    db.timetable.insert_one(d)