from consts import *
from user import User


# TODO: implement language processing model
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

    def __init__(self, week, name, time, participants=None, kind=None, day=None, hour=None):
        if participants is None:
            participants = []
        if not kind:
            # if kind was not given - we generate it based on the assignment name
            kind = generate_kind(name, time)
        self.__week = week
        self.__name = name
        self.__kind = kind
        self.__day = day
        self.__hour = hour
        self.__time = time
        self.__participants = participants

    def get_time(self):
        return self.__time

    def set_time(self, time):
        self.__time = time

    def get_week(self):
        return self.__week

    def get_name(self):
        return self.__name

    def get_kind(self):
        return self.__kind

    def get_day(self):
        return self.__day

    def get_hour(self):
        return self.__hour

    def get_participants(self):
        return self.__participants

    def add_participant(self, user: User):
        self.__participants.append(user)

        # changes the kind to meeting because there are participants now:
        self.set_kind(kinds["MEETING"])

    def set_participants(self, participants):
        self.__participants = participants

        # changes the kind to meeting because there are participants now:
        self.set_kind(kinds["MEETING"])

    def set_week(self, week: int):
        self.__week = week

    def set_name(self, name: int):
        self.__name = name

    def set_kind(self, kind: int):
        self.__kind = kind

    def set_day(self, day: int):
        self.__day = day

    def set_hour(self, hour: int):
        self.__hour = hour

    def is_overlap(self, other):
        """
            checks if 2 assignments are overlap
        """

        if self.get_day() is None or self.get_hour() is None or other.get_day() is None or other.get_hour() is None:
            raise ValueError("day or hour have not been initialized in Assignment.is_overlap")

        if self.get_week() != other.get_week() or self.get_day() != other.get_day():
            return False

        x1 = self.get_hour()
        x2 = x1 + self.get_time()
        y1 = other.get_hour()
        y2 = y1 + other.get_time()

        return 


