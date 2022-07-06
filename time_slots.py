import numpy as np
from consts import *
from time_ import Time


def find_possible_slots(duration, time_slots_list, lunches, must_be, consts):
    """
    finding all the time intervals of length duration which are possible in all the time slots in the list
    :param duration: the duration
    :param time_slots_list: all the time slots
    :return: [(day, x1, x2) - list of time intervals and their days]
    """
    free_slots = []
    before_meeting = max([const.get_hard_constraints()["break before meeting"] for const in consts])
    before_must_be = max([const.get_hard_constraints()["break before must be"] for const in consts])
    after_meeting = max([const.get_hard_constraints()["break after meeting"] for const in consts])
    after_must_be = max([const.get_hard_constraints()["break after must be"] for const in consts])
    for i in range((DAYS-2) * (HOURS-1) * QUARTERS):
        free = True
        for time_slot in time_slots_list:
            if not time_slot.check_all_available(1+i // (HOURS * QUARTERS), 1+(i % (HOURS * QUARTERS)) // QUARTERS,
                                                 i % QUARTERS, duration):
                free = False
            start_time = Time(h=1 + (i % (HOURS * QUARTERS)) // QUARTERS, m=(i % QUARTERS) * 15)-before_meeting
            finish_time = start_time+duration+after_meeting
            for start, end in must_be:
                if Time.is_overlap(start_time, finish_time, start-before_must_be, end+after_must_be):
                    free = False
            # consistent with lunch:
            start_time = Time(h=1 + (i % (HOURS * QUARTERS)) // QUARTERS, m=(i % QUARTERS) * 15)
            finish_time = start_time + duration
            for (start, finish, duration_lunch) in lunches:
                if (start_time < start or duration_lunch > (start_time-start)) and (finish<finish_time or duration_lunch > finish-finish_time):
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

