import datetime


def format_duration(duration_str):
    hours = 0
    minutes = 0
    seconds = 0

    if 'H' in duration_str:
        hours = int(duration_str.split('T')[-1].split('H')[0])
        duration_str = duration_str.split('H')[-1]

    if 'M' in duration_str:
        if 'H' in duration_str:
            minutes = int(duration_str.split('H')[-1].split('M')[0])
            duration_str = duration_str.split('M')[-1]
        else:
            minutes = int(duration_str.split('T')[-1].split('M')[0])
            duration_str = duration_str.split('M')[-1]

    if 'S' in duration_str:
        if 'M' in duration_str:
            seconds = int(duration_str.split('M')[-1].split('S')[0])
        elif 'H' in duration_str:
            seconds = int(duration_str.split('H')[-1].split('S')[0])
        else:
            seconds = int(duration_str.split('T')[-1].split('S')[0])

    time = datetime.timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )

    duration = str(time).split(":")
    if duration[0] == "0":
        return str(time)[2:]
    else:
        return str(time)


print(format_duration("PT1H56M51S"))
print(format_duration("T02M04S"))
print(format_duration("T49S"))