import numpy as np

from time_slots import find_possible_slots


class GradientDecent:
    def __init__(self, week, meetings, free_times, kind, users):
        self.__week = week
        self.__meetings = meetings
        self.__free_times = free_times
        self.__kind = kind
        self.__users = users
        # setting the meetings as scheduled:
        for m in self.__meetings:
            for u in m.get_participants():
                u.move_to_scheduled(week, m)

    def score(self, scores):
        if self.__kind == "sum":
            return sum(scores)
        elif self.__kind == "equal":
            """
            maximizing the equality == minimizing the std
            """
            return -np.std(np.array(scores))

    def solve(self):
        optional_slots = [[] for _ in range(len(self.__meetings))] # optional slots for every meeting
        for i in self.__meetings.keys():
            time_slots = [self.__free_times[k]["free slots"] for k in self.__meetings[i]["participants"]]
            optional_slots[i] += find_possible_slots(self.__meetings[i]["duration"], time_slots)

