from dateutil.parser import parse
from datetime import datetime

class MediaDate:
    DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"

    def __init__(self, stringDate, origin):
        self.date = self.__parse(stringDate)
        self.origin = origin

    def toFileName(self):
        return self.date.strftime('%Y-%m-%d_%H.%M.%S')

    def getOrigin(self):
        return self.origin

    def getYear(self):
        return self.date.strftime('%Y')

    def __parse(self, stringDate):
        normalisedDate = self.__normaliseStringDate(stringDate)
        return datetime.strptime(normalisedDate, self.DATETIME_FORMAT)

    def __normaliseStringDate(self, stringDate):
        if self.__hasTime(stringDate):
            normalisedDate = stringDate
        else:
            normalisedDate = stringDate + " 00:00:00"
        return self.__excludeTimeZoneInfo(normalisedDate)

    def __excludeTimeZoneInfo(self, stringDate):
        return stringDate[0:19]

    def __hasTime(self, stringDate):
        return " " in stringDate

    def __str__(self):
        return self.date.strftime('%Y:%m:%d %H:%M:%S')
