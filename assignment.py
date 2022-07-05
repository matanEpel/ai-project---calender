from consts import *
from datetime import datetime, timedelta



# TODO: implement language processing model
from time_ import *


def generate_kind(name, time):
    """
    Generates a kind based on language processing model.
    Sets the kind to the output of the model.
    :return: none
    """

    return kinds["TASK"]


class Assignment:
    """
    The basic Assignment class.
    The class defines all the properties of an assignment - week, name,
    kind, day and hour.
    All the stuff here is pretty straight forward except for the use of generate_kind
    function which is the "AI" part of this class
    """

    def __init__(self, week, name, duration, participants=None, kind=None, day=None, time=None):
        if participants is None:
            participants = []
        if not kind:
            # if kind was not given - we generate it based on the assignment name
            kind = generate_kind(name, duration)
        self.__week = week
        self.__name = name
        self.__kind = kind
        self.__day = day
        self.__time = time  # time of beginning
        self.__duration = duration  # duration of event
        self.__participants = participants
        self.__curr_day =  BASELINE_DAY

    def get_time(self):
        return self.__time

    def get_duration(self):
        return self.__duration

    def get_week(self):
        return self.__week

    def get_name(self):
        return self.__name

    def get_kind(self):
        return self.__kind

    def get_day(self):
        return self.__day

    def get_participants(self):
        return self.__participants

    def get_curr_day(self):
        return self.__curr_day

    def add_participant(self, user):
        self.__participants.append(user)

        # changes the kind to meeting because there are participants now:
        self.set_kind(kinds["MEETING"])

    def set_participants(self, participants):
        self.__participants = participants

        # changes the kind to meeting because there are participants now:
        self.set_kind(kinds["MEETING"])

    def set_week(self, week: int):
        self.__week = week

    def set_duration(self, duration):
        self.__duration = duration

    def set_name(self, name: int):
        self.__name = name

    def set_kind(self, kind: int):
        self.__kind = kind

    def set_day(self, day: int):
        self.__day = day

    def set_time(self, time):
        self.__time = time

    def update_curr(self):
        days = (self.__week - 1) * 7 + (self.__day - 1)
        d = timedelta(days=days)
        self.__curr_day += d

    def to_datetime_time(self):
        self.update_curr()
        start_hours = self.get_time().get_hours()
        start_minutes = self.get_time().get_minutes()

        end_time = self.get_time() + self.get_duration()
        end_hours = end_time.get_hours()
        end_minutes = end_time.get_minutes()

        start_time = datetime.strptime(f"{start_hours}:{start_minutes}", "%H:%M").time()
        end_time = datetime.strptime(f"{end_hours}:{end_minutes}", "%H:%M").time()
        date = self.get_curr_day()

        start = datetime.combine(date, start_time)
        end = datetime.combine(date, end_time)

        return start, end




    def __str__(self):
        return "name: {}, starting at {}, for {} at day {},week {}".format(
            self.__name, str(self.__time), str(self.__duration), self.__day, self.__week)

    def is_overlap(self, other):
        """
            checks if 2 assignments are overlap
        """

        if self.get_day() is None or self.get_hour() is None or other.get_day() is None or other.get_hour() is None:
            raise ValueError("day or hour have not been initialized in Assignment.is_overlap")

        if self.get_week() != other.get_week() or self.get_day() != other.get_day():
            return False

        t1 = self.get_time()
        t2 = t1 + self.get_duration()
        t3 = other.get_time()
        t4 = t3 + other.get_duration()

        return Time.is_overlap(t1, t2, t3, t4)


