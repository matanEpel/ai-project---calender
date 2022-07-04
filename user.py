import itertools
import random
from copy import deepcopy
from typing import Dict, Tuple

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

    def get_all_assignments(self):
        final = []
        for week in self.__assignments.keys():
            final += self.__assignments[week]
        return final

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

    def schedule_week(self, week: int, SHUFFLE=True):
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

        # schedule the assignments
        assignments_array = [a for a in self.get_assignments(week) if a.get_kind() == consts.kinds["TASK"]]
        duration_array = [a.get_duration() for a in assignments_array]

        self.assignments_map = list(enumerate(duration_array))  # map between assignments

        schedule = self.csp_schedule_assignment(week=week, SHUFFLE=SHUFFLE)
        for s in schedule.items():
            assignments_array[s[0][0]].set_time(s[1][0])
            assignments_array[s[0][0]].set_day(s[1][1])
            self.place_assignment(assignments_array[s[0][0]], week=week)
        return self.__constraints.calculate_score(self.__schedule[week])
        """
            kinds = {"TASK": 0, "MEETING": 1, "MUST_BE_IN": 2}, every MEETING and MUST_BE_IN comes immediatly with time.
        """

    def place_assignment(self, assignment: Assignment, week: int):
        if assignment.get_time() is None or assignment.get_day() is None:
            raise ValueError("assignment cannot be placed")

        # TODO need to check if slot is available

        self.__schedule[week].append(assignment)

    def csp_schedule_assignment(self, week, SHUFFLE):
        """
            in order to reduce memory and time, we get only array of durations and match them to the assignments by index.
            VARIABLES - self.assignments_map - [(0, duration), (1, duration), ...]
            DOMAIN - available_times_days
            CONSTRAINTS -
        """
        starting_times = list()  # variables
        available_times = Time.get_range(self.get_constraints().get_hard_constraints()["start of the day"],
                                         self.get_constraints().get_hard_constraints()["end of the day"])
        self.times_domain = list(itertools.product(available_times,
                                                   self.get_constraints().get_hard_constraints()[
                                                       "working days"]))  # domain
        if SHUFFLE:
            random.shuffle(self.times_domain)

        # for t in self.assignments_map:
        #     print(t)
        # for t in self.times_domain:  # DEBUG
        #     print("time {}, d {}".format(str(t[0]), t[1]))

        return self.backtrack_search(week=week)

    def backtrack_search(self, week, assigned_variables_dict: Dict[Tuple[int, Time], Tuple[Time, int]] = {}):
        """
            times_dict -
        """
        if len(assigned_variables_dict) == len(self.assignments_map):
            # every assignment has starting_time
            return assigned_variables_dict

        # print("BACKTRACK")
        # print(self.assignments_map)
        # print(assigned_variables_dict)
        unassigned_variables = [v for v in self.assignments_map if v not in assigned_variables_dict.keys()]

        # chose the variable with the largest duration
        max_dur = Time()
        current_var = unassigned_variables[0]

        for var in unassigned_variables:
            if var[1] > max_dur:
                max_dur = var[1]
                current_var = var

        # current_var = unassigned_variables[0]  # Chooses the first, can in the future choose a random value

        for time in self.times_domain:  # can iterate randomly on the time domain in order to make the back track random
            local_assigned_variables_dict = assigned_variables_dict.copy()
            local_assigned_variables_dict[current_var] = time
            if self.consistent(local_assigned_variables_dict, week=week):
                # NEED TO WRITE self.consistent
                result = self.backtrack_search(week=week, assigned_variables_dict=local_assigned_variables_dict)
                if result is not None:
                    return result

        return None

    def consistent(self, assigned_variables_dict: Dict[Tuple[int, Time], Tuple[Time, int]], week):
        """
            need to check if the assignment is legal by all of the constraints
            need to take into considiration:
            1. self.__constraints
            2. the assignements which already been asigned
            3. the MEETINGS and MUST BE events
        """
        for day in self.get_constraints().get_hard_constraints()["working days"]:
            intervals = [(x[1][0], x[0][1] + x[1][0]) for x in list(assigned_variables_dict.items()) if x[1][1] == day]

            s = self.__schedule[week]
            meetings_intervals = [(m.get_time(), m.get_time() + m.get_duration()) for m in self.__schedule[week] if
                                  m.get_day() == day]
            if Time.is_list_overlap(intervals=intervals + meetings_intervals):
                return False

            if Time.max_time(intervals) > self.get_constraints().get_hard_constraints()["end of the day"]:
                return False

        # preform more many checks ....

        for var in assigned_variables_dict:
            pass

        return True
