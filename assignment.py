from consts import *
from user import *


class Assignment:
    """
    The basic Assignment class.
    The class defines all the properties of an assignment - week, name,
    kind, day and hour.
    All the stuff here is pretty straight forward except for the generate_kind
    function which is the "AI" part of this class
    """

    def __init__(self, week, name, participants=None, kind=None, day=None, hour=None):
        if participants is None:
            participants = []
        self.__week = week
        self.__name = name
        self.__kind = kind
        self.__day = day
        self.__hour = hour
        self.__participants = participants

    def generate_kind(self):
        """
        Generates a kind based on language processing model.
        Sets the kind to the output of the model.
        :return: none
        """
        self.__kind = kinds["TASK"]

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
        self.set_kind(kinds["MEETING"])

    def set_participants(self, participants):
        self.__participants = participants
        self.set_kind(kinds["MEETING"])

    def set_week(self, week):
        self.__week = week

    def set_name(self, name):
        self.__name = name

    def set_kind(self, kind):
        self.__kind = kind

    def set_day(self, day):
        self.__day = day

    def set_hour(self, hour):
        self.__hour = hour
