from typing import List

import numpy as np

from assignment import Assignment
from time_ import Time
from consts import kinds


class Constraints:
    def __init__(self):
        # defining all the default hard constraints values (can be changed)
        self.__hard_constraints = dict()
        self.__hard_constraints["overlap meeting task"] = False
        self.__hard_constraints["overlap must be task"] = False
        self.__hard_constraints["lunch time"] = (Time(h=11),Time(h=16),Time(h=0,m=30)) # range for launch and time of launch
        self.__hard_constraints["break before meeting"] = Time() # done
        self.__hard_constraints["break before task"] = Time() # done
        self.__hard_constraints["break before must be"] = Time() # done
        self.__hard_constraints["break after meeting"] = Time(m=15) # done
        self.__hard_constraints["break after task"] = Time(m=15) # done
        self.__hard_constraints["break after must be"] = Time() # done
        self.__hard_constraints["start of the day"] = Time(h=8)  # done
        self.__hard_constraints["end of the day"] = Time(h=22)  # done
        self.__hard_constraints["working days"] = [1, 2, 3, 4, 5]  # done

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

    def calculate_score(self, week_schedule: List[Assignment]):
        """

        :param week_schedule:
        :return:
        """
        week_schedule = {i: sorted([ass for ass in week_schedule if ass.get_day() == i], key=lambda ass: ass.get_time())
                         for i in range(1,8)}
        start_late = 0
        finish_early = 0
        close_meetings = 0
        close_tasks = 0
        continuous_breaks = 0

        for day in range(1,8):
            continuous_breaks_in_day = 0
            if len(week_schedule[day]) != 0:
                day_sorted = sorted(week_schedule[day], key=lambda a:a.get_time())
                start_late += day_sorted[0].get_time().get_hours()+week_schedule[day][0].get_time().get_minutes()/60
                start_late -= self.__hard_constraints["start of the day"].get_hours()
                finish_early += self.__hard_constraints["end of the day"].get_hours()
                finish_early -= (day_sorted[-1].get_time().get_hours() + day_sorted[-1].get_time().get_minutes()/60)
            for i in range(len(week_schedule[day])-1):
                if week_schedule[day][i].get_kind() == kinds["TASK"] and \
                   week_schedule[day][i+1].get_kind() == kinds["TASK"]:
                    close_tasks += 1
                if week_schedule[day][i].get_kind() == kinds["MEETING"] and\
                   week_schedule[day][i+1].get_kind() == kinds["MEETING"]:
                    close_meetings += 1
                if week_schedule[day][i+1].get_time() > \
                   week_schedule[day][i].get_time() + week_schedule[day][i].get_duration():
                    time = week_schedule[day][i+1].get_time() - \
                                         (week_schedule[day][i].get_duration() + week_schedule[day][i].get_time())
                    continuous_breaks_in_day = np.max([time.get_hours() + time.get_minutes()/60, continuous_breaks_in_day])
            continuous_breaks += continuous_breaks_in_day
        start_late_max = len(self.__hard_constraints["working days"])*(self.__hard_constraints["lunch time"][0]-self.__hard_constraints["start of the day"]).get_hours()
        end_early_max = start_late_max
        continuous_breaks_max = start_late_max
        close_meetings_max = (len([a for day in week_schedule for a in week_schedule[day] if a.get_kind() == kinds["MEETING"]])-1)
        close_tasks_max = (len([a for day in week_schedule for a in week_schedule[day] if a.get_kind() == kinds["TASK"]]) - 1)
        score = start_late/start_late_max*self.__soft_constraints["start the day late"]
        score += finish_early/end_early_max*self.__soft_constraints["finish the day early"]
        score += close_meetings/close_meetings_max*self.__soft_constraints["meetings are close together"]
        score += close_tasks/close_tasks_max*self.__soft_constraints["tasks are close together"]
        score += continuous_breaks/continuous_breaks_max*self.__soft_constraints["breaks are continuous"]
        score /= (sum([np.abs(self.__soft_constraints[c]) for c in self.__soft_constraints]))
        # print(" | ".join([", ".join([str(a) for a in week_schedule[i]]) for i in week_schedule]), score)
        return score
