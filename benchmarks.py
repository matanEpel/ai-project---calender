from copy import deepcopy
import time
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


def default_users2(manager):
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
    meeting2 = Assignment(week=1, name="m3", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir, matan])
    meeting3 = Assignment(week=1, name="m4", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir, matan])
    meeting4 = Assignment(week=1, name="m5", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir, matan])
    # for the genetic first test - remove 4 meetings

    ofir.add_assignment(assignment)
    ofir.add_assignment(assignment2)
    ofir.add_assignment(assignment3)
    ofir.add_assignment(assignment4)
    ofir.add_assignment(assignment5)
    ofir.add_assignment(meeting)
    ofir.add_assignment(meeting2)
    ofir.add_assignment(meeting3)
    ofir.add_assignment(meeting4)
    matan.add_assignment(deepcopy(assignment))
    matan.add_assignment(deepcopy(assignment2))
    matan.add_assignment(deepcopy(assignment3))
    matan.add_assignment(deepcopy(assignment4))
    matan.add_assignment(deepcopy(assignment5))
    manager.add_user(ofir, 1)
    manager.add_user(matan, 1)
    return ofir, matan


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


def create_graph_grad(manager):
    manager.set_type("gradient")
    manager.set_gradient_type("LOW_MEETINGS")
    manager.set_epochs(50)
    manager.schedule_week(1)
    dist_from_start = [1, 2, 3, 4, 5]
    epoch_1 = [1.0337975547181826, 1.2709904089171502, 1.2709904089171502, 1.2709904089171502,
               1.2709904089171502]  # these are the prints from manager.schedule_week(1)
    epoch_2 = [1.02621679129132, 1.177323309389699, 1.2791288322353713, 1.2791288322353713,
               1.2791288322353713]  # we have 5 epochs so 5 graphs
    epoch_3 = [1.010132703995185, 1.2310085056599, 1.2554289546793669, 1.2831073761876413, 1.2831073761876413]
    epoch_4 = [1.0293847189239755, 1.2073508783693905, 1.266572257766962, 1.266572257766962, 1.266572257766962]
    epoch_5 = [1.0259728736940579, 1.2315123741487253, 1.4135945953460378, 1.4728839840419385, 1.4728839840419385]
    plt.plot(dist_from_start, [round(a, 2) for a in epoch_1])
    plt.plot(dist_from_start, [round(a, 2) for a in epoch_2])
    plt.plot(dist_from_start, [round(a, 2) for a in epoch_3])
    plt.plot(dist_from_start, [round(a, 2) for a in epoch_4])
    plt.plot(dist_from_start, [round(a, 2) for a in epoch_5])
    plt.title("score by distance from start point - 5 different runs")
    plt.xlabel("distance from start")
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
    mustbe1 = Assignment(week=1, name="mb1", duration=Time(m=30), kind=kinds["MUST_BE_IN"], time=Time(h=11), day=1)
    mustbe2 = Assignment(week=1, name="mb2", duration=Time(h=1, m=15), kind=kinds["MUST_BE_IN"], time=Time(h=15), day=2)
    mustbe3 = Assignment(week=1, name="mb3", duration=Time(h=2), kind=kinds["MUST_BE_IN"], time=Time(h=18), day=3)
    mustbe4 = Assignment(week=1, name="mb4", duration=Time(h=3, m=15), kind=kinds["MUST_BE_IN"], time=Time(h=9), day=4)
    mustbe5 = Assignment(week=1, name="mb5", duration=Time(m=15), kind=kinds["MUST_BE_IN"], time=Time(h=11), day=5)

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
        output_list.append(avg_score / 10)

        print(i)

    print(output_list)
    print(u)

    plt.plot(x_list, output_list)
    plt.title("Avg max score vs number of calls to random CSP")
    plt.xlabel("num of calls")
    plt.ylabel("avg max score")
    plt.show()


def test_running_times_grad(manager):
    times = []
    manager.set_type("gradient")
    manager.set_gradient_type("LOW_MEETINGS")
    manager.set_epochs(1)
    ofir, matan = default_users2(manager)
    meeting = Assignment(week=1, name="m2", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir, matan])
    for i in range(10):
        print(i, "----------")
        new = deepcopy(meeting)
        new.set_name("m" + str(3 + i))
        manager.get_users()[0].add_assignment(new)

        start = time.time()
        manager.schedule_week(1)
        end = time.time()
        times.append(end - start)
    plt.plot(list(range(1, 11)), times)
    plt.title("gradient ascent running times as function of meetings")
    plt.xlabel("meetings")
    plt.ylabel("running time [s]")
    plt.show()


def test_running_times_gen(manager):
    times = []
    manager.set_type("genetic")
    manager.set_gradient_type("LOW_MEETINGS")
    manager.set_epochs(2)
    ofir, matan = default_users2(manager)
    meeting = Assignment(week=1, name="m2", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir, matan])
    for i in range(10):
        print(i, "----------")
        new = deepcopy(meeting)
        new.set_name("m" + str(3 + i))
        manager.get_users()[0].add_assignment(new)

        start = time.time()
        manager.schedule_week(1)
        end = time.time()
        times.append(end - start)
    plt.plot(list(range(1, 11)), times)
    plt.title("genetic running times as function of meetings")
    plt.xlabel("meetings")
    plt.ylabel("running time [s]")
    plt.show()


def test_running_times_start_points(manager):
    times = []
    manager.set_type("genetic")
    manager.set_gradient_type("LOW_MEETINGS")
    manager.set_epochs(2)
    ofir, matan = default_users2(manager)
    meeting = Assignment(week=1, name="m2", duration=Time(h=1), kind=kinds["MEETING"], participants=[ofir, matan])
    new = deepcopy(meeting)
    new.set_name("m" + str(3 + 1))
    manager.get_users()[0].add_assignment(new)
    new = deepcopy(meeting)
    new.set_name("m" + str(3 + 2))
    manager.get_users()[0].add_assignment(new)
    new = deepcopy(meeting)
    new.set_name("m" + str(3 + 3))
    manager.get_users()[0].add_assignment(new)
    for i in range(2, 30, 2):
        print(i, "----------")
        manager.set_genetic_start_point(i)

        start = time.time()
        manager.schedule_week(1)
        end = time.time()
        times.append(end - start)
    plt.plot(list(range(2, 30, 2)), times)
    plt.title("genetic running times as function of starting points")
    plt.xlabel("starting point")
    plt.ylabel("running time [s]")
    plt.show()


def main():
    # get out of documentation in order to run the needed benchmark
    # meetings benchmarks:
    manager = Manager()

    n = input("which test you want to run?\n1. genetic algorithm score test\n2. gradient decent score test\n3. genetic running times - meetings"
              "\n4. genetic running times - starting points\n5. gradient running times\n6. CSOP score")
    if n == "1":
        default_users(manager)
        create_score("genetic", "LOW_MEETINGS", manager, 1, [i for i in range(1,20)])
    if n == "2":
        default_users(manager)
        create_graph_grad(manager)
    if n == "3":
        test_running_times_gen(manager)
    if n == "4":
        test_running_times_start_points(manager)
    if n == "5":
        test_running_times_grad(manager)
    if n == "6":
        test_task_assignments()


if __name__ == '__main__':
    main()
