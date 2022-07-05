import random

import numpy as np

from copy import deepcopy
from consts import EPOCHS, THRESHOLD_LOT_OF_MEETS
from time_ import Time
from time_slots import find_possible_slots


class GradientDecent:
    def __init__(self, week, meetings, free_times, kind, users):
        self.__week = week
        self.__meetings = meetings
        self.__free_times = free_times
        self.__kind = kind
        self.__users = users
        if len(self.__meetings) >= THRESHOLD_LOT_OF_MEETS:
            self.__mode = "HIGH_MEETINGS"
        else:
            self.__mode = "LOW_MEETINGS"

    def score(self, scores):
        if self.__kind == "sum":
            return sum(scores)
        elif self.__kind == "equal":
            """
            maximizing the equality == minimizing the std
            """
            return -np.std(np.array(scores))

    def solve_epoch(self, optional_slots, num):
        time_for_each_meeting = self.get_random_start_point(
            optional_slots)  # [(day, time) - list of times for the meetings]
        prev_score = -np.inf
        new_score = -np.inf
        # doing the gradient decent part
        curr_final_users = deepcopy(self.__users)
        count_in = 0
        while new_score > prev_score or new_score == -np.inf:
            count_in += 1
            for i in range(len(self.__meetings)):
                self.__meetings[i]["object"].set_day(time_for_each_meeting[i][0])
                self.__meetings[i]["object"].set_time(time_for_each_meeting[i][1])
            scores = [user.schedule_week(self.__week) for user in self.__users]
            max = self.score(scores)
            new_times = time_for_each_meeting
            for_final_users = deepcopy(self.__users)
            count_for = 0
            for new_times_for_each_meeting in self.get_neighbor_times(optional_slots, time_for_each_meeting):
                print(num, count_in, count_for)
                count_for += 1
                # print(new_times_for_each_meeting)
                for i in range(len(self.__meetings)):
                    self.__meetings[i]["object"].set_day(new_times_for_each_meeting[i][0])
                    self.__meetings[i]["object"].set_time(new_times_for_each_meeting[i][1])
                scores = [user.schedule_week(self.__week) for user in self.__users]
                if self.score(scores) > max:
                    for_final_users = deepcopy(self.__users)
                    max = self.score(scores)
                    # print(max)

                    new_times = new_times_for_each_meeting

            prev_score = new_score
            new_score = max
            if new_score > prev_score:
                curr_final_users = for_final_users
                time_for_each_meeting = new_times
        return new_score, prev_score, curr_final_users

    def solve(self):
        # get all possible slots for each meeting:
        optional_slots = [[] for _ in range(len(self.__meetings))]  # optional slots for every meeting
        for i in self.__meetings.keys():
            time_slots = [self.__free_times[k]["free slots"] for k in self.__meetings[i]["participants"]]
            optional_slots[i] += find_possible_slots(self.__meetings[i]["duration"], time_slots)

        final_time_for_each_meeting = []
        final_score = -np.inf
        final_users = deepcopy(self.__users)

        # in case of a lot of meetings the neighbors are pretty random so we want a lot of epochs:
        # in case of low meetings we are checking all the neighbors of someone so it's pretty
        epochs_amount = EPOCHS
        if self.__mode == "LOW_MEETINGS":
            epochs_amount = EPOCHS//10
        # trying X different starting points:
        for _ in range(epochs_amount):
            # get random starting point:
            new_score, prev_score, curr_final_users = self.solve_epoch(optional_slots, _)
            if np.max([new_score, prev_score]) > final_score:
                final_users = curr_final_users
                final_score = np.max([new_score, prev_score])
                print(final_score)
        self.__users = final_users
        print("score", final_score)
        return self.__users

    def get_random_start_point(self, optional_slots, idx):
        slots = []
        for slots_of_day in optional_slots:
            available_slots = []
            for curr_slot in slots_of_day:
                available = True
                for slot in slots:
                    if curr_slot["day"] == slot["day"] and Time.is_overlap(curr_slot["start"], curr_slot["finish"],
                                                                           slot["start"], slot["finish"]):
                        available = False
                if available:
                    available_slots.append(curr_slot)
            slot = random.choice(available_slots)
            slots.append(slot)

        return [(s["day"], s["start"]) for s in slots]

    def high_meetings_neighbors(self, time_for_each_meeting, optional_slots):
        all_options = []
        for i in range(len(time_for_each_meeting)):
            for j in range(i + 1, len(time_for_each_meeting)):
                new_option = time_for_each_meeting[:i] + [time_for_each_meeting[j]] + time_for_each_meeting[i + 1:j] + [
                    time_for_each_meeting[i]] + time_for_each_meeting[j + 1:]
                if self.is_consistent(new_option, optional_slots):
                    all_options.append(new_option)
        return all_options

    def low_meetings_neighbors(self, time_for_each_meeting, optional_slots):
        all_options = []
        for i in range(len(time_for_each_meeting)):
            for j in range(len(optional_slots[i])):
                new_option = time_for_each_meeting[:i] + [(optional_slots[i][j]["day"], optional_slots[i][j]["start"])] + time_for_each_meeting[i + 1:]
                if self.is_consistent(new_option, optional_slots):
                    all_consistent = True
                    for i in range(len(new_option)):
                        for j in range(i + 1, len(new_option)):
                            if new_option[i][0] == new_option[j][0] and Time.is_overlap(new_option[i][1],new_option[i][1]+self.__meetings[i]["duration"], new_option[j][1],new_option[j][1]+self.__meetings[j]["duration"]):
                                all_consistent = False
                    if all_consistent:
                        all_options.append(new_option)
        return all_options

    def get_neighbor_times(self, optional_slots, time_for_each_meeting):
        """
        the neighbors are all the optional switches between the slots
        :param optional_slots:
        :param time_for_each_meeting:
        :return:
        """
        # when we have a lot of meetings and can't look at all the possibilities for each meeting
        if self.__mode == "HIGH_MEETINGS":
            return self.high_meetings_neighbors(time_for_each_meeting, optional_slots)
        elif self.__mode == "LOW_MEETINGS":
            return self.low_meetings_neighbors(time_for_each_meeting, optional_slots)

    def is_consistent(self, option, optional_slots):
        for i in range(len(option)):
            time = option[i]
            day = time[0]
            time_in_day = time[1]
            if all([time_in_day != slot["start"] for slot in optional_slots[i] if slot["day"] == day]):
                return False
        return True
