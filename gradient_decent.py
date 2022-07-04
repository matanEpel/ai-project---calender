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

        time_for_each_meeting = self.get_random_start_point(optional_slots) # [(day, time) - list of times for the meetings]
        for i in range(len(self.__meetings)):
            self.__meetings[i]["object"].set_day(time_for_each_meeting[0])
            self.__meetings[i]["object"].set_time(time_for_each_meeting[1])
        scores = [user.schedule_week(self.__week) for user in self.__users]
        prev_score = -np.inf
        new_score = self.score(scores)
        while new_score > prev_score:
            max = -np.inf
            new_times = []
            for new_times_for_each_meeting in self.get_neighbors_time(optional_slots, time_for_each_meeting):
                for i in range(len(self.__meetings)):
                    self.__meetings[i]["object"].set_day(time_for_each_meeting[0])
                    self.__meetings[i]["object"].set_time(time_for_each_meeting[1])
                scores = [user.schedule_week(self.__week) for user in self.__users]
                if self.score(scores) > max:
                    max = self.score(scores)
                    new_times = new_times_for_each_meeting
            prev_score = new_score
            new_score = max
            if new_score > prev_score:
                time_for_each_meeting = new_times
        for i in range(len(self.__meetings)):
            self.__meetings[i]["object"].set_day(time_for_each_meeting[0])
            self.__meetings[i]["object"].set_time(time_for_each_meeting[1])


