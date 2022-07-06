from copy import deepcopy

from assignment import Assignment
from constraint import Constraints
from consts import kinds, EPOCHS
from manager import Manager
from time_ import Time
from user import User
import matplotlib.pyplot as plt

def default_users(manager):
    c = Constraints()
    c.set_soft_constraint("meetings are close together", 1000)
    c2 = Constraints()
    c2.set_soft_constraint("start the day late", 1000)
    ofir = User("Ophir", c)
    matan = User("Matan", c2)

    assignment = Assignment(week=1, name="ex1", duration=Time(h=1), kind=kinds["TASK"])
    assignment2 = Assignment(week=1, name="ex2", duration=Time(h=1), kind=kinds["TASK"])
    assignment3 = Assignment(week=1, name="ex3", duration=Time(h=1), kind=kinds["TASK"])
    assignment4 = Assignment(week=1, name="ex4", duration=Time(h=1), kind=kinds["TASK"])
    assignment5 = Assignment(week=1, name="ex4", duration=Time(h=1), kind=kinds["TASK"])
    meeting = Assignment(week=1, name="m2", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir, matan])
    meeting2 = Assignment(week=1, name="m2", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir, matan])
    meeting3 = Assignment(week=1, name="m3", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir, matan])
    meeting4 = Assignment(week=1, name="m3", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir, matan])
    meeting5 = Assignment(week=1, name="m3", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir, matan])

    ofir.add_assignment(assignment)
    ofir.add_assignment(assignment2)
    ofir.add_assignment(assignment3)
    ofir.add_assignment(assignment4)
    ofir.add_assignment(assignment5)
    ofir.add_assignment(meeting)
    ofir.add_assignment(meeting2)
    ofir.add_assignment(meeting3)
    ofir.add_assignment(meeting4)
    ofir.add_assignment(meeting5)
    matan.add_assignment(deepcopy(assignment))
    matan.add_assignment(deepcopy(assignment2))
    matan.add_assignment(deepcopy(assignment3))
    matan.add_assignment(deepcopy(assignment4))
    matan.add_assignment(deepcopy(assignment5))
    # matan.add_assignment(meeting)
    # matan.add_assignment(meeting2)
    # matan.add_assignment(meeting3)
    manager.add_user(ofir, 1)
    manager.add_user(matan, 1)



def create_score(kind, grad_kind, manager, week, epochs):
    scores = []
    manager.set_type(kind)
    manager.set_gradient_type(grad_kind)
    for e in epochs:
        print(e, "-------")
        manager.set_epochs(e)
        scores.append(manager.schedule_week(week))
    plt.plot(epochs, scores)
    plt.title(kind + " algorithm: score vs epochs")
    plt.xlabel("epochs")
    plt.ylabel("score")
    plt.show()

def test_task_assignments():
    c = Constraints()
    c.set_soft_constraint("tasks are close together", 1000)
    c.set_soft_constraint("start the day late", 1000)
    u = User("User", c)

    assignment1 = Assignment(week=1, name="ex1", duration=Time(h=1, m=30), kind=kinds["TASK"])
    assignment2 = Assignment(week=1, name="ex2", duration=Time(h=2), kind=kinds["TASK"])
    assignment3 = Assignment(week=1, name="ex3", duration=Time(h=2), kind=kinds["TASK"])
    assignment4 = Assignment(week=1, name="ex4", duration=Time(h=3), kind=kinds["TASK"])
    assignment5 = Assignment(week=1, name="ex5", duration=Time(h=2), kind=kinds["TASK"])
    assignment6 = Assignment(week=1, name="ex6", duration=Time(h=1, m=30), kind=kinds["TASK"])
    assignment7 = Assignment(week=1, name="ex7", duration=Time(h=2), kind=kinds["TASK"])
    assignment8 = Assignment(week=1, name="ex8", duration=Time(h=2), kind=kinds["TASK"])
    assignment9 = Assignment(week=1, name="ex9", duration=Time(h=3), kind=kinds["TASK"])
    assignment10 = Assignment(week=1, name="ex10", duration=Time(h=2), kind=kinds["TASK"])
    mustbe1 = Assignment(week=1, name="mb1", duration=Time(m=30), kind=kinds["MUST_BE_IN"], time = Time(h=11), day=1)
    mustbe2 = Assignment(week=1, name="mb2", duration=Time(h=1, m=15), kind=kinds["MUST_BE_IN"], time = Time(h=15), day=2)
    mustbe3 = Assignment(week=1, name="mb3", duration=Time(h=2), kind=kinds["MUST_BE_IN"], time = Time(h=18), day=3)
    mustbe4 = Assignment(week=1, name="mb4", duration=Time(h=3, m=15), kind=kinds["MUST_BE_IN"], time = Time(h=9), day=4)
    mustbe5 = Assignment(week=1, name="mb5", duration=Time(m=15), kind=kinds["MUST_BE_IN"], time = Time(h=11), day=5)

    ass_list = [assignment1, assignment2, assignment3, assignment4, assignment5, assignment6, assignment7,
                assignment8, assignment9, assignment10, mustbe1, mustbe2, mustbe3, mustbe4, mustbe5]

    for a in ass_list:
        u.add_assignment(a)

    output_list = []
    x_list = []
    N = 100

    for i in range(1, N):
        avg_score = 0
        x_list.append(i)
        for j in range(10):
            avg_score += u.schedule_week_with_optimal(1, n=i)
        output_list.append(avg_score/10)

        print(i)

    print(output_list)
    print(u)

    plt.plot(x_list, output_list)
    plt.title("Avg max score vs number of calls to random CSP")
    plt.xlabel("num of calls")
    plt.ylabel("avg max score")
    plt.show()
    plt.save("avg max score")



def main():
    # meetings benchmarks:
    # manager = Manager()
    # default_users(manager)
    # create_score("genetic", "LOW_MEETINGS", manager, 1, [i for i in range(1,20)])
    # create_score("gradient", "LOW_MEETINGS", manager, 1, [i*10 for i in range(1,20)])
    # create_score("gradient", "HIGH_MEETINGS", manager, 1, [i for i in range(1,20)])
    pass



if __name__ == '__main__':
    test_task_assignments()
