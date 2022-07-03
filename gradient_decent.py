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

    def solve(self):
        pass
