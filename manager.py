from consts import kinds, QUARTERS, HOURS, DAYS
from user import User
from time_slots import TimeSlots
from gradient_decent import *
from genetic_algorithm import *
from search import *


def get_users(meetings):
    users = []
    for m in meetings:
        for u in m.get_participants():
            if u not in users:
                users.append(u)
    return users


def genetic_solution(week, meetings, free_times, kind, users, mode, weights):
    solver = GeneticAlgorithm(week, meetings, free_times, kind, users, weights)
    return solver.solve()


def gradient_solution(week, meetings, free_times, kind, users, mode, weights):
    solver = GradientDecent(week, meetings, free_times, kind, users, mode, weights)
    return solver.solve()


class Manager:
    def __init__(self, type="genetic", kind="sum", grad_type="low"):
        self.__type = type
        self.__kind = kind
        self.__grad_type = grad_type
        self.__users = []
        self.__weights = []

    def __repr__(self):
        return "Manager with " + str(len(self.__users)) + " users: " + "\n".join([u.get_name() for u in self.__users])

    def get_users(self):
        return self.__users

    def add_user(self, user: User, weight):
        self.__users.append(user)
        self.__weights.append(weight)

    def del_user(self, user: User):
        if user in self.__users:
            self.__users.remove(user)

    def set_type(self, type):
        self.__type = type

    def set_kind_of_optimization(self, kind):
        self.__kind = kind

    def set_gradient_type(self, grad_type):
        self.__grad_type = grad_type

    def schedule_week(self, week):
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
        print("sdkfjsdkfjdskf")
        # DEBUG
        # for u in self.__users:
        #     u.schedule_week_with_optimal(week)
        # return
        if self.__type == "genetic":
            self.__users = genetic_solution(*self.get_data(week, self.__kind, self.__users, self.__grad_type))
        elif self.__type == "gradient":
            self.__users = gradient_solution(*self.get_data(week, self.__kind, self.__users, self.__grad_type))

    def schedule_week_user(self, week: int, user: User):
        """
        schedule the tasks of a specific user in specific week
        takes all of the assignments in user and sets for them a day and an houer
        returns the score of the scheduling
        """
        # need to iterate over ~20 options with different BLOCKS in order to get different results and choose the best one.
        return user.schedule_week(week)

    def get_data(self, week, kind, users, grad_type):
        meetings = {}
        free_times = []
        data_slots_dict = {}
        user_count = 0
        meeting_count = 0
        for user in users:
            free_slots = TimeSlots()
            for ass in user.get_assignments(week):
                # create meeting dict
                if ass.get_kind() == kinds["MEETING"]:
                    participants = []
                    for participant in ass.get_participants():
                        for i in range(len(users)):
                            if participant.get_name() == users[i].get_name():
                                participants.append(i)
                    add = True
                    for key in meetings:
                        if ass == meetings[key]["object"] and participants == meetings[key]["participants"]:
                            add = False
                    if add:
                        meetings[meeting_count] = {"object": ass, "duration": ass.get_duration(),
                                                   "participants": participants}
                    meeting_count += 1
                # create time slots for each user
                elif ass.get_kind() == kinds["MUST_BE_IN"]:
                    duration = ass.get_duration()
                    day = ass.get_day()
                    hour = ass.get_time().get_hours()
                    quarter = ass.get_time().get_minutes() // 15
                    for i in range(int(duration.get_hours() * 4 + duration.get_minutes() // 15)):
                        free_slots.set_unavailable(day + (hour * QUARTERS + quarter + i) // (QUARTERS * HOURS),
                                                   hour + (quarter + i) // QUARTERS, (quarter + i) % QUARTERS)
            for day in range(1, DAYS + 1 - 2):
                for i in range(
                        (-1 + user.get_constraints().get_hard_constraints()["start of the day"].get_hours()) * 4):
                    free_slots.set_unavailable(day, 1 + i // QUARTERS, i % QUARTERS)
                for i in range((25 - user.get_constraints().get_hard_constraints()["end of the day"].get_hours()) * 4):
                    free_slots.set_unavailable(day, user.get_constraints().get_hard_constraints()[
                        "end of the day"].get_hours() + i // QUARTERS, i % QUARTERS)
                lunch = user.get_constraints().get_hard_constraints()["lunch time"]

            data_slots_dict[user_count] = {"user": user, "free slots": free_slots}
            user_count += 1
        """
        meeting:
        dict which contains numbered meetings:
        idx: assignment, duration, list of indexed participants
        
        data_slots_dict:
        dict of the free times and the user of each idx
        idx: user, its free times
        """
        return week, meetings, data_slots_dict, kind, users, grad_type, self.__weights
