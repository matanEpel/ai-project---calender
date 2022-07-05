import numpy as np
from consts import *
from time_ import Time


def find_possible_slots(duration, time_slots_list):
    """
    finding all the time intervals of length duration which are possible in all the time slots in the list
    :param duration: the duration
    :param time_slots_list: all the time slots
    :return: [(day, x1, x2) - list of time intervals and their days]
    """
    free_slots = []
    for i in range((DAYS-2) * (HOURS-1) * QUARTERS):
        free = True
        for time_slot in time_slots_list:
            if not time_slot.check_all_available(1+i // (HOURS * QUARTERS), 1+(i % (HOURS * QUARTERS)) // QUARTERS,
                                                 i % QUARTERS, duration):
                free = False
        if free:
            free_slots.append({"day": 1+i // (HOURS * QUARTERS),
                               "start": Time(h=1+(i % (HOURS * QUARTERS)) // QUARTERS, m=(i % QUARTERS) * 15),
                               "finish": Time(h=1+(i % (HOURS * QUARTERS)) // QUARTERS,
                                              m=(i % QUARTERS) * 15) + duration})
    return free_slots


class TimeSlots:
    """
    Object which defines the available time slots in a day
    """

    def __init__(self):
        self.__slots = np.array([[1] * QUARTERS * HOURS] * (DAYS-2))

    def set_unavailable(self, day, hour, quarter):
        self.__slots[day - 1, (hour - 1) * 4 + quarter] = 0

    def set_available(self, day, hour, quarter):
        self.__slots[day - 1, (hour - 1) * 4 + quarter] = 1

    def check_available(self, day, hour, quarter):
        return self.__slots[day - 1, (hour - 1) * 4 + quarter] == 1

    def check_all_available(self, day, hour, quarter, duration):
        hours = duration.get_hours()
        minutes = duration.get_minutes()
        for i in range(int(hours * 4 + minutes // 15)):
            if not self.check_available(day + (hour * QUARTERS + quarter + i) // (QUARTERS * HOURS),
                                        hour + (quarter + i) // QUARTERS, (quarter + i) % QUARTERS):
                return False
        return True

