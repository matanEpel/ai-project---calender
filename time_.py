from __future__ import annotations

from copy import deepcopy
from typing import Tuple


class Time:

    def __init__(self, h=0, m=0):
        if h < 0 or h > 24 or m < 0 or m >= 59:
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
        q, r = divmod(minutes, 60)
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
    def is_list_overlap(intervals: list[Tuple[Time, Time]]) -> bool:
        """
            intervals - list of tuples that stands for init time and duration
        """
        #TODO i think this algorithm can be improved using a data structure like tims_slots
        for i in range(len(intervals)):
            for j in range(len(intervals)):
                if i == j:
                    continue
                l1 = intervals[i]
                l2 = intervals[j]
                if Time.is_overlap(l1[0], l1[1], l2[0], l2[1]):
                    return True

        return False





if __name__ == "__main__":
    print(Time.get_range(Time(h=8), Time(h=12)))

