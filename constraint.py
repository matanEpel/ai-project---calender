from consts import kinds


class Constraints:
    def __init__(self):
        # defining all the default hard constraints values (can be changed)
        self.__hard_constraints = dict()
        self.__hard_constraints["overlapping meetings"] = False
        self.__hard_constraints["overlapping tasks"] = False
        self.__hard_constraints["overlapping must be"] = False
        self.__hard_constraints["overlap meeting task"] = False
        self.__hard_constraints["overlap meeting must be"] = False
        self.__hard_constraints["overlap must be task"] = False
        self.__hard_constraints["must be is must be"] = True
        self.__hard_constraints["break before meeting"] = 0
        self.__hard_constraints["break before task"] = 0
        self.__hard_constraints["break before must be"] = 0
        self.__hard_constraints["break after meeting"] = 0
        self.__hard_constraints["break after task"] = 0
        self.__hard_constraints["break after must be"] = 0
        self.__hard_constraints["start of the day"] = 8
        self.__hard_constraints["end of the day"] = 22
        self.__hard_constraints["working days"] = [1, 2, 3, 4, 5]

        # defining all the soft constraints weight (each constraint has a weight which defines it's importance)
        # for each time a soft constraint is satisfied - the user gives it 1 point normalized
        # with the weight of the constraint
        self.__soft_constraints = dict()
        self.__soft_constraints["meetings are close together"] = 1  # one point for each 2 continuous meetings
        self.__soft_constraints["tasks are close together"] = 1  # one point for each 2 continuous tasks
        self.__soft_constraints["breaks are continuous"] = 1  # one point for each continuous hour of break
        self.__soft_constraints["finish the day early"] = 1  # one point for each hour of finishing early
        self.__soft_constraints["start the day late"] = 1  # one point for each hour of starting late

    def get_hard_constraints_options(self):
        return self.__hard_constraints.keys()

    def get_hard_constraints(self):
        return self.__hard_constraints

    def set_hard_constraint(self, name, value):
        self.__hard_constraints[name] = value

    def set_soft_constraint(self, name, value):
        self.__soft_constraints[name] = value

    def calculate_score(self, week_schedule):
        start_late = 0
        finish_early = 0
        close_meetings = 0
        close_tasks = 0
        continuous_breaks = 0

        for day in range(1,8):
            if len(week_schedule[day]) != 0:
                start_late += week_schedule[day][0].get_hour()-self.__hard_constraints["start of the day"]
                finish_early += self.__hard_constraints["end of the day"] - (week_schedule[day][-1].get_hour() +
                                                                             week_schedule[day][-1].get_time())
            for i in range(len(week_schedule[day])-1):
                if week_schedule[day][i].get_kind() == kinds["TASK"] and \
                   week_schedule[day][i+1].get_kind() == kinds["TASK"]:
                    close_tasks += 1
                if week_schedule[day][i].get_kind() == kinds["MEETING"] and\
                   week_schedule[day][i+1].get_kind() == kinds["MEETING"]:
                    close_meetings += 1
                if week_schedule[day][i+1].get_hour() > \
                   week_schedule[day][i].get_hour() + week_schedule[day][i].get_time():
                    continuous_breaks += week_schedule[day][i+1].get_hour() - \
                                         (week_schedule[day][i].get_hour() + week_schedule[day][i].get_time())
        score = start_late*self.__soft_constraints["start the day late"]
        score += finish_early*self.__soft_constraints["finish the day early"]
        score += close_meetings*self.__soft_constraints["meetings are close together"]
        score += close_tasks*self.__soft_constraints["tasks are close together"]
        score += continuous_breaks*self.__soft_constraints["breaks are continuous"]
        score /= (sum([self.__soft_constraints[c] for c in self.__soft_constraints]))
        return score
