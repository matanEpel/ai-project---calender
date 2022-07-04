from assignment import Assignment
from manager import Manager
from time_ import *
from consts import kinds
from time_slots import find_possible_slots
from user import User
from constraint import Constraints

def main_epel():
    a1 = Assignment(week=1, name="ex1", duration=Time(h=1), kind=kinds["TASK"])
    a2 = Assignment(week=1, name="ex2", duration=Time(h=4), kind=kinds["MEETING"])
    a3 = Assignment(week=1, name="ex3", duration=Time(h=2), kind=kinds["MUST_BE_IN"], day=2, time=Time(h=10))
    a4 = Assignment(week=1, name="ex3", duration=Time(h=2, m=31), kind=kinds["MUST_BE_IN"], day=2, time=Time(h=11))
    a5 = Assignment(week=1, name="ex3", duration=Time(h=2), kind=kinds["MUST_BE_IN"], day=3, time=Time(h=10))
    consts = Constraints()
    user = User("matan", consts)
    user.add_assignment(a1)
    user.add_assignment(a2)
    user.add_assignment(a3)
    user.add_assignment(a4)
    user.add_assignment(a5)
    manager = Manager()
    manager.add_user(user)
    a = manager.get_data(1, "sum", manager.get_users())
    slots = [a[2][k]["free slots"] for k in a[2]]
    a = find_possible_slots(Time(h=2, m=33), slots)
    print(a)

def main_amit():
    """
        random staff for debuging
    """
    c = Constraints()
    c.set_soft_constraint("meetings are close together", 100)
    # c.set_soft_constraint("tasks are close together", 100)
    ofir = User("Ofir", c)
    matan = User("matan", c)
    amit = User("amit", c)

    a1 = Assignment(week=1, name="ex1", duration=Time(h=1), kind=kinds["TASK"])
    a2 = Assignment(week=1, name="ex2", duration=Time(h=1), kind=kinds["TASK"])
    a3 = Assignment(week=1, name="ex3", duration=Time(h=1), kind=kinds["TASK"])
    a4 = Assignment(week=1, name="ex4", duration=Time(h=1), kind=kinds["TASK"])
    a5 = Assignment(week=1, name="ex5", duration=Time(h=1), kind=kinds["TASK"])
    a6 = Assignment(week=1, name="ex6", duration=Time(h=2), kind=kinds["TASK"])
    a7 = Assignment(week=1, name="ex7", duration=Time(h=3), kind=kinds["TASK"])
    a8 = Assignment(week=1, name="ex8", duration=Time(h=2), kind=kinds["TASK"])
    a9 = Assignment(week=1, name="ex9", duration=Time(h=1), kind=kinds["TASK"])
    a10 = Assignment(week=1, name="ex10", duration=Time(h=1), kind=kinds["TASK"])
    a11 = Assignment(week=1, name="ex11", duration=Time(h=5), kind=kinds["TASK"])

    b1 = Assignment(week=1, name="m1", duration=Time(h=2), kind=kinds["MEETING"])
    b2 = Assignment(week=1, name="m2", duration=Time(h=2), kind=kinds["MEETING"])
    b3 = Assignment(week=1, name="m3", duration=Time(h=4), kind=kinds["MEETING"])
    mb1 = Assignment(week=1, name="mb1", duration=Time(h=2, m=30), kind=kinds["MUST_BE_IN"], day = 1, time=Time(h=9,m=30))
    mb2 = Assignment(week=1, name="mb2", duration=Time(h=2), kind=kinds["MUST_BE_IN"], day = 2, time=Time(h=10,m=30))
    mb3 = Assignment(week=1, name="mb3", duration=Time(h=2), kind=kinds["MUST_BE_IN"], day = 1, time=Time(h=13,m=15))

    ofir.add_assignment(a1)
    ofir.add_assignment(a2)
    ofir.add_assignment(a3)
    ofir.add_assignment(a4)
    ofir.add_assignment(a5)
    ofir.add_assignment(b1)
    ofir.add_assignment(b2)
    ofir.add_assignment(b3)

    manager = Manager()
    manager.add_user(ofir)
    manager.schedule_week(1)
    for u in manager.get_users():
        print(u)
    # print(ofir)
    #print(ofir.get_schedule(1))




if __name__ == '__main__':
    main_amit()
    # main_epel()
