import datetime

def transferTime(timeString):
    x = datetime.datetime.strptime(timeString,'%Y-%m-%dT%H:%M:%S+0000')
    return x