from datetime import datetime
from dateutil import tz
from datetime import timezone

def removeHtmlTags(string):
    string = string.replace('\\r', '')
    string = string.replace('\\t', '')
    string = string.replace('\\n', '')
    string = string.replace('<br>', '')
    return string

def convertTime(base):

    # METHOD 2: Auto-detect zones:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # utc = datetime.utcnow()
    #utc = datetime.strptime('2011-01-21 02:37:21', '%Y-%m-%d %H:%M:%S')
    print(base)
    base = base[:25].strip()
    utc = datetime.strptime(base, '%a, %d %b %Y %H:%M:%S')
    #Mon, 1 Oct 2018 22:35:03 +0000 (UTC)

    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    central = utc.astimezone(to_zone)
    return central
    #return central.strftime('%Y-%m-%d')
    #return central.strftime('%a, %d %b %Y %H:%M:%S %z')

def find_nth(string, substring, n):
   if (n == 1):
       return string.find(substring)
   else:
       return string.find(substring, find_nth(string, substring, n - 1) + 1)