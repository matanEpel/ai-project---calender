import numpy as np
from consts import *


class TimeSlots:
    """
    Object which defines the available time slots in a day
    """
    def __init__(self):
        self.__slots = np.array([[1] * QUARTERS * HOURS] * DAYS)

    def set_unavailable(self, day, hour, quarter):
        self.__slots[day-1, (hour-1)*4+quarter] = 0

    def set_available(self, day, hour, quarter):
        self.__slots[day-1, (hour-1)*4+quarter] = 1

    def check_available(self, day, hour, quarter):
        return self.__slots[day-1, (hour-1)*4+quarter] == 1

    def check_all_available(self, day, hour, quarter, duration):
        for i in range(int(duration*4)):
            if not self.check_available(day + (hour*QUARTERS+quarter + i) // (QUARTERS * HOURS),
                                        hour + (quarter + i) // QUARTERS, (quarter + i) % QUARTERS):
                return False
        return True

