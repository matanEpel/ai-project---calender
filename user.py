from assignment import *


class User:
    """
    The user class. Every user include its name, and all of his tasks for
    every week. Additionally, it includes the schedule for all the tasks
    of of each week.
    """
    def __init__(self, name: str):
        self.__name = name
        self.__assignments = dict()

        # schedule is a dict of assignments for every week that must include an hour attached to them
        self.__schedule = dict()

    def set_name(self, name: str):
        self.__name = name

    def get_name(self):
        return self.__name

    def add_assignment(self, assignment: Assignment):
        self.__assignments[assignment.get_week()].append(assignment)

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
        self.__schedule[week] = self.__assignments[week]
