from __future__ import annotations
import numpy as np
from copy import deepcopy
from typing import Tuple


class Time:

    def __init__(self, h=0, m=0):
        if h < 0 or m < 0 or m >= 59:
            raise ValueError("hours or minutes are not in range")
        self.hours = h
        self.minutes = m

    def get_hours(self):
        return self.hours

    def get_minutes(self):
        return self.minutes

    def set_minutes(self, m):
        self.minutes = m

    def set_hours(self, h):
        self.hours = h

    def __deepcopy__(self, memodict={}):
        return Time(h=self.get_hours(), m=self.get_minutes())

    def __add__(self, other):
        hours = self.get_hours() + other.get_hours()
        minutes = self.get_minutes() + other.get_minutes()
        q, r =  divmod(minutes, 60)
        return Time(hours + q, r)

    def __sub__(self, other):
        hours = self.get_hours() - other.get_hours()
        minutes = self.get_minutes() - other.get_minutes()
        q, r = divmod(minutes, 60)
        return Time(hours + q, r)

    def __iadd__(self, other):
        hours = self.get_hours() + other.get_hours()
        minutes = self.get_minutes() + other.get_minutes()
        q, r = divmod(minutes, 60)
        self.set_hours(hours + q)
        self.set_minutes(r)

    def __eq__(self, other):
        """
            define the operator ==
        """
        return self.get_hours() == other.get_hours() and self.get_minutes() == other.get_minutes()

    def __hash__(self):
        return hash(self.get_hours() * self.get_minutes())

    def __lt__(self, other):
        """
            define the operator <
        """
        if self.get_hours() < other.get_hours():
            return True

        if self.get_hours() > other.get_hours():
            return False

        if self.get_minutes() < other.get_minutes():
            return True

        if self.get_minutes() > other.get_minutes():
            return False

        # if arrived here, they are equals
        return False

    def __le__(self, other):
        """
            define the operator <=
        """
        if self == other:
            return True

        return self < other

    def __str__(self):
        return "{}:{}".format(self.hours, self.minutes)

    def __repr__(self):
        return "{}:{}".format(self.hours, self.minutes)

    @staticmethod
    def get_next(t):
        """
            adds 15 minutes to the time
        """
        return t + Time(m=15)

    @staticmethod
    def get_range(t_s, t_f):
        """
            returns a range of times with jumps of 15m
            [t_s, t_f)
        """
        t = deepcopy(t_s)
        time_range = list()
        while t != t_f:
            time_range.append(t)
            t = Time.get_next(t)

        return time_range


    @staticmethod
    def is_overlap(x1, x2, y1, y2):
        """
            checks if the the 2 intervals [x1, x2] and [y1, y2] are overlapping
        """
        return x1 < y2 and y1 < x2

    @staticmethod
    def is_list_overlap(intervals: list[Tuple[Time, Time]], s1: Time = None, s2: Time = None) -> bool:
        """
            intervals - list of tuples that stands for init time and duration
        """
        #TODO i think this algorithm can be improved using a data structure like tims_slots

        # for i in range(len(intervals)):
        #     for j in range(len(intervals)):
        #         if i == j:
        #             continue
        #         l1 = intervals[i]
        #         l2 = intervals[j]
        #         if Time.is_overlap(l1[0], l1[1], l2[0], l2[1]):
        #             return True
        #
        # return False

        intervals = sorted(intervals, key=lambda x: x[0])
        for i in range(len(intervals) - 1):
            if intervals[i][1] > intervals[i + 1][0]:
                return True

        return False

        # d = DaySlots(s1, s2)
        # for interval in intervals:
        #     if d.mark_slot(interval[0], interval[1]):
        #         return True
        #
        # return False





    @staticmethod
    def max_time(intervals: list[Tuple[Time, Time]]) -> Time:
        max_end_time = Time()

        for t in intervals:
            if t[1] > max_end_time:
                max_end_time = t[1]

        return max_end_time


# class DaySlots:
#     """
#     Object which defines the available time slots in a day
#     """
#
#     def __init__(self, s1: Time, s2: Time):
#         self.s1 = s1
#         self.s2 = s2
#         delta = s2 - s1
#         self.n = int(delta.get_hours() * 4 + (delta.get_minutes() / 15))
#         print(self.n)
#         self.__slots = np.zeros(self.n)
#
#     def mark_slot(self, start_time: Time, duration: Time):
#         start_index = self.get_index(start_time)
#         end_index = start_index + self.get_range(duration)
#         for i in range(self.get_index(start_time), end_index):
#             if self.__slots[i] == 1:
#                 return True
#             self.__slots[i] = 1
#
#         print(self.__slots)
#         return False
#
#     def get_index(self, time: Time):
#         delta = time - self.s1
#         return int(delta.get_hours() * 4 + (delta.get_minutes() / 15))
#
#     def get_range(self, time: Time):
#         return int(time.get_hours() * 4 + time.get_minutes() / 15)


if __name__ == "__main__":
    print(Time.get_range(Time(h=8), Time(h=12)))

