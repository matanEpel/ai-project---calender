import consts
from assignment import *
from constraint import *
from time_ import Time


class User:
    """
    The user class. Every user include its name, and all of his tasks for
    every week. Additionally, it includes the schedule for all the tasks
    of of each week.
    """

    def __init__(self, name: str, constraints: Constraints):
        self.__name = name
        self.__assignments = dict()  # tasks

        # schedule is a dict of assignments for every week that must include an hour attached to them
        self.__schedule = dict()

        self.__constraints = constraints

    def set_name(self, name: str):
        self.__name = name

    def get_name(self):
        return self.__name

    def add_assignment(self, assignment: Assignment):
        if assignment.get_week() in self.__assignments.keys():
            self.__assignments[assignment.get_week()].append(assignment)
        else:
            self.__assignments[assignment.get_week()] = [assignment]  # creates a list

    def remove_assignment(self, assignment: Assignment):
        """
        removes an assignment from the assignmets of the user
        :param assignment: name of the assignment
        :return: none
        """
        week = assignment.get_week()
        if week in self.__assignments and assignment in self.__assignments[week]:
            self.__assignments[week].remove(assignment)
        if week in self.__schedule and assignment in self.__schedule[week]:
            self.__schedule[week].remove(assignment)

        # schedule must be changed if we modified our assignments in order to be optimal
        del self.__schedule[week]

    def get_assignments(self, week: int):
        return self.__assignments[week]

    def get_schedule(self, week: int):
        return self.__schedule[week]

    def set_schedule(self, week: int):
        """
        This function copies all the assignment of a week into the schedule dict
        It basically means that the manager has modified the hours and days of every assignment
        so it is now in a scheduled form
        :param week: the week that was scheduled
        :return: none
        """
        self.__schedule[week] = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        for ass in self.__assignments[week]:
            self.__schedule[week][ass.get_day()].append(ass)

    def set_constrains(self, constraints):
        self.__constraints = constraints

    def get_constraints(self):
        return self.__constraints

    def __str__(self):
        # TODO currently for debuging prints only week §
        output = "[User] {}\nassignments:\n".format(self.__name)
        for a in self.__assignments[1]:
            output += str(a)
            output += "\n"

        output += "\nschedule:\n"
        for a in self.__schedule[1]:
            output += str(a)
            output += "\n"

        return output



    def schedule_week(self, week: int):
        """
            schedule the tasks of a specific user in specific week
            takes all of the assignments in user and sets for them a day and an houer

            return constraints.get_score()
        """

        #  only for now, not csp yet
        self.__schedule[week] = list()
        for a in self.get_assignments(week):
            if a.get_kind() == consts.kinds["MEETING"] or a.get_kind() == consts.kinds["MUST_BE_IN"]:
                self.place_assignment(a, week)

        for a in self.get_assignments(week):
            if a.get_kind() == consts.kinds["TASK"]:
                self.greedy_schedule_assignment(a, week)

        """
            kinds = {"TASK": 0, "MEETING": 1, "MUST_BE_IN": 2}, every MEETING and MUST_BE_IN comes immediatly with time.
        """

    def place_assignment(self, assignment: Assignment, week: int):
        if assignment.get_time() is None or assignment.get_day() is None:
            raise ValueError("assignment cannot be placed")

        # TODO need to check if slot is available

        self.__schedule[week].append(assignment)

    def greedy_schedule_assignment(self, assignment: Assignment, week: int):
        duration = assignment.get_duration()
        # TODO place at the first available slot
        assignment.set_day(1)
        assignment.set_time(Time(h=9))
        self.__schedule[week].append(assignment)



