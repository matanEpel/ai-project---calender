import random
from copy import deepcopy

import numpy as np

from consts import AMOUNT_STARTING_POINTS, GENETIC_EPOCHS, AMOUNT_TO_DIVIDE
from time_ import Time
from time_slots import find_possible_slots


class GeneticAlgorithm:
    def __init__(self, week, meetings, free_times, kind, users):
        self.__amount_of_epochs = GENETIC_EPOCHS
        self.__week = week
        self.__meetings = meetings
        self.__free_times = free_times
        self.__kind = kind
        self.__users = users
        self.__amount_of_starting_points = AMOUNT_STARTING_POINTS

    def score(self, scores):
        if self.__kind == "sum":
            return sum(scores)
        elif self.__kind == "equal":
            """
            maximizing the equality == minimizing the std
            """
            return -np.std(np.array(scores))

    def solve(self):
        optional_slots = [[] for _ in range(len(self.__meetings))]  # optional slots for every meeting
        for i in self.__meetings.keys():
            time_slots = [self.__free_times[k]["free slots"] for k in self.__meetings[i]["participants"]]
            optional_slots[i] += find_possible_slots(self.__meetings[i]["duration"], time_slots)
        time_pool = [self.get_start_point(optional_slots) for _ in
                     range(self.__amount_of_starting_points)]  # [(day, time) - list of times for the meetings]
        for _ in range(self.__amount_of_epochs):
            solutions = []
            for i in range(len(time_pool)):
                new_times_for_each_meeting = time_pool[i]
                for j in range(len(self.__meetings)):
                    self.__meetings[i]["object"].set_day(new_times_for_each_meeting[j][0])
                    self.__meetings[i]["object"].set_time(new_times_for_each_meeting[j][1])
                scores = [user.schedule_week(self.__week) for user in self.__users]
                solutions.append({"meetings": new_times_for_each_meeting, "users": deepcopy(self.__users),
                                  "score": self.score(scores)})
            if _ == self.__amount_of_epochs - 1:
                best = max(solutions, key=lambda s: s["score"])
                max_users = best["users"]
                max_score = best["score"]
                self.__users = max_users
                return max_score
            else:
                remaining_solutions = sorted(solutions, key=lambda s: s["score"], reverse=True)
                remaining_solutions = remaining_solutions[:self.__amount_of_starting_points]
                time_pool = []
                for i in range(len(remaining_solutions)):
                    for j in range(i + 1, len(remaining_solutions)):
                        time_pool += self.children_and_mutation(remaining_solutions[i], remaining_solutions[j],
                                                                optional_slots)

    def get_start_point(self, optional_slots):
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

    def children_and_mutation(self, meetings_1, meetings_2, optional_slots):
        children = self.children(meetings_1, meetings_2, optional_slots)
        return self.mutation(children, optional_slots)

    def is_consistent(self, option, optional_slots):
        for i in range(len(option)):
            time = option[i]
            day = time[0]
            time_in_day = time[1]
            if all([time_in_day != slot["start"] for slot in optional_slots[i] if slot["day"] == day]):
                return False
        return True

    def children(self, meetings_1, meetings_2, optional_slots):
        options = []
        # switching between times of meetings
        for i in range(len(meetings_1)):
            opt1 = meetings_2[:i] + [meetings_1[i]] + meetings_2[i + 1:]
            opt2 = meetings_1[:i] + [meetings_2[i]] + meetings_1[i + 1:]
            if self.is_consistent(opt1, optional_slots):
                options.append(opt1)
            if self.is_consistent(opt2, optional_slots):
                options.append(opt2)
        return options

    def get_random_point(self, optional_slots, idx, other_slots):
        slots_of_day = optional_slots[idx]
        available_slots = []
        for curr_slot in slots_of_day:
            available = True
            for slot in other_slots:
                if curr_slot["day"] == slot["day"] and Time.is_overlap(curr_slot["start"], curr_slot["finish"],
                                                                       slot["start"], slot["finish"]):
                    available = False
            if available:
                available_slots.append(curr_slot)
        if not len(available_slots):
            return None
        slot = random.choice(available_slots)
        return slot

    def mutation(self, childrens, optional_slots):
        final = []

        for child in childrens:
            idx = random.choice(list(range(len(child))))
            new_loc = self.get_random_point(optional_slots, idx, child[:idx] + child[idx + 1:])
            if new_loc:
                final.append(child[:idx] + [new_loc] + child[idx + 1:])

        return final
