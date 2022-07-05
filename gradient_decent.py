import random

import numpy as np

from copy import deepcopy
from consts import EPOCHS
from time_ import Time
from time_slots import find_possible_slots


class GradientDecent:
    def __init__(self, week, meetings, free_times, kind, users):
        self.__week = week
        self.__meetings = meetings
        self.__free_times = free_times
        self.__kind = kind
        self.__users = users

    def score(self, scores):
        if self.__kind == "sum":
            return sum(scores)
        elif self.__kind == "equal":
            """
            maximizing the equality == minimizing the std
            """
            return -np.std(np.array(scores))

    def solve(self):
        # get all possible slots for each meeting:
        optional_slots = [[] for _ in range(len(self.__meetings))] # optional slots for every meeting
        for i in self.__meetings.keys():
            time_slots = [self.__free_times[k]["free slots"] for k in self.__meetings[i]["participants"]]
            optional_slots[i] += find_possible_slots(self.__meetings[i]["duration"], time_slots)

        final_time_for_each_meeting = []
        final_score = -np.inf

        final_users = deepcopy(self.__users)
        # trying X different starting points:
        for _ in range(EPOCHS):
            print(_)
            # get random starting point:
            time_for_each_meeting = self.get_random_start_point(optional_slots) # [(day, time) - list of times for the meetings]
            prev_score = -np.inf
            new_score = -np.inf
            # doing the gradient decent part
            curr_final_users = deepcopy(self.__users)
            count_in = 0
            while new_score > prev_score or new_score == -np.inf:
                print("\t",count_in)
                count_in += 1
                for i in range(len(self.__meetings)):
                    self.__meetings[i]["object"].set_day(time_for_each_meeting[i][0])
                    self.__meetings[i]["object"].set_time(time_for_each_meeting[i][1])
                scores = [user.schedule_week(self.__week) for user in self.__users]
                max = self.score(scores)
                new_times = time_for_each_meeting
                for_final_users = deepcopy(self.__users)
                for new_times_for_each_meeting in self.get_neighbor_times(optional_slots, time_for_each_meeting):
                    # print(new_times_for_each_meeting)
                    for i in range(len(self.__meetings)):
                        self.__meetings[i]["object"].set_day(time_for_each_meeting[i][0])
                        self.__meetings[i]["object"].set_time(time_for_each_meeting[i][1])
                    scores = [user.schedule_week(self.__week) for user in self.__users]
                    if self.score(scores) > max:
                        for_final_users = deepcopy(self.__users)
                        max = self.score(scores)

                        new_times = new_times_for_each_meeting

                prev_score = new_score
                new_score = max
                if new_score > prev_score:
                    curr_final_users = for_final_users
                    time_for_each_meeting = new_times

            if np.max([new_score, prev_score]) > final_score:
                final_users = curr_final_users
                final_score = np.max([new_score, prev_score])
                print(final_score)
        self.__users = final_users
        print("score", final_score)
        return self.__users


    def get_random_start_point(self, optional_slots):
        slots = []
        for slots_of_day in optional_slots:
            available_slots = []
            for curr_slot in slots_of_day:
                available = True
                for slot in slots:
                    if curr_slot["day"] == slot["day"] and Time.is_overlap(curr_slot["start"], curr_slot["finish"], slot["start"], slot["finish"]):
                        available = False
                if available:
                    available_slots.append(curr_slot)
            slot = random.choice(slots_of_day)
            slots.append(slot)

        return [(s["day"], s["start"]) for s in slots]

    def get_neighbor_times(self, optional_slots, time_for_each_meeting):
        """
        the neighbors are all the optional switches between the slots
        :param optional_slots:
        :param time_for_each_meeting:
        :return:
        """
        all_options = []
        for i in range(len(time_for_each_meeting)):
            for j in range(i+1,len(time_for_each_meeting)):
                new_option = time_for_each_meeting[:i] + [time_for_each_meeting[j]] + time_for_each_meeting[i+1:j] + [time_for_each_meeting[i]] + time_for_each_meeting[j+1:]
                if self.is_consistent(new_option, optional_slots):
                    all_options.append(new_option)
        return all_options

    def is_consistent(self, option, optional_slots):
        for i in range(len(option)):
            time = option[i]
            day = time[0]
            time_in_day = time[1]
            if all([time_in_day != slot["start"] for slot in optional_slots[i] if slot["day"] == day]):
                return False
        return True



