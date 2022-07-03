from consts import kinds, QUARTERS, HOURS
from user import User
from time_slots import TimeSlots


def genetic_solution(meetings, free_times, kind):
    return [(1, 1, 1, 1)]


def gradient_solution(meetings, free_times, kind):
    return [(1, 1, 1, 1)]


def search_solution(meetings, free_times, kind):
    return [(1, 1, 1, 1)]


class Manager:
    def __init__(self):
        self.__users = []

    def get_users(self):
        return self.__users

    def add_user(self, user: User):
        self.__users.append(user)

    def del_user(self, user: User):
        if user in self.__users:
            self.__users.remove(user)

    def set_solution(self, week, assignments_assigned):
        """
        Sets the assignment of the assignments as the schedule of the week
        for every user.
        :param week: the week we edit
        :param assignments_assigned: the assignments we assigned
        :return: none
        """
        for user, ass, day, hour in assignments_assigned:
            ass.set_day(day)
            ass.set_hour(hour)
            user.move_to_scheduled(week, ass)

    def schedule_week(self, week, type, kind):
        """
        schedules the week of all the users together - uses three different algorithms:
        1. genetic algorithm
        2. linear programming
        3. classic search with heuristics
        :param week: the week we are working on
        :param type: the type of solution we want
        :param kind: the kind of equilibrium we want. The types are:
        1. as equal as possible - finding the position which maximizes on the solution to be as fair
        as possible for all users
        2. best overall - finding the solution which maximizes on the sum of scores
        :return:
        """
        if type == "genetic":
            self.set_solution(week, genetic_solution(*self.get_data(week, kind)))
        elif type == "gradient":
            self.set_solution(week, gradient_solution(*self.get_data(week, kind)))
        elif type == "search":
            self.set_solution(week, search_solution(*self.get_data(week, kind)))

    def schedule_week_user(self, week: int, user: User):
        """
        schedule the tasks of a specific user in specific week
        takes all of the assignments in user and sets for them a day and an houer
        returns the score of the scheduling
        """
        return user.schedule_week(week)

    def get_data(self, week, kind):
        meetings = []
        free_times = []
        for user in self.__users:
            free_slots = TimeSlots()
            for ass in user.get_assignments(week):
                if ass.get_kind() == kinds["MEETING"]:
                    meetings.append((ass, ass.get_name(), ass.get_time()))
                elif ass.get_kind() == kinds["MUST_BE_IN"]:
                    duration = ass.get_duration()
                    day = ass.get_time().get_day()
                    hour = ass.get_time().get_hour()
                    quarter = ass.get_time().get_minute() // 4
                    for i in range(int(duration * 4)):
                        free_slots.set_unavailable(day + (hour * QUARTERS + quarter + i) // (QUARTERS * HOURS),
                                                   hour + (quarter + i) // HOURS, (quarter + i) % HOURS)
            free_times.append((user, free_slots))

        return meetings, free_times, kind
