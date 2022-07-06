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
def main():
    # meetings benchmarks:
    manager = Manager()
    default_users(manager)
    create_score("genetic", "LOW_MEETINGS", manager, 1, [i for i in range(1,20)])
    create_score("gradient", "LOW_MEETINGS", manager, 1, [i*10 for i in range(1,20)])
    create_score("gradient", "HIGH_MEETINGS", manager, 1, [i for i in range(1,20)])



if __name__ == '__main__':
    main()
