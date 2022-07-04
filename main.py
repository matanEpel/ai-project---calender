from assignment import Assignment
from time_ import *
from consts import kinds
from user import User
from constraint import Constraints

def main():
    """
        random staff for debuging
    """

    a1 = Assignment(week=1, name="ex1", duration=Time(h=1), kind=kinds["TASK"])
    a2 = Assignment(week=1, name="ex2", duration=Time(h=4), kind=kinds["TASK"])
    a3 = Assignment(week=1, name="ex3", duration=Time(h=2), kind=kinds["TASK"])
    a4 = Assignment(week=1, name="ex4", duration=Time(h=5), kind=kinds["TASK"])
    a5 = Assignment(week=1, name="ex5", duration=Time(h=6), kind=kinds["TASK"])
    a6 = Assignment(week=1, name="ex6", duration=Time(h=2), kind=kinds["TASK"])
    a7 = Assignment(week=1, name="ex7", duration=Time(h=3), kind=kinds["TASK"])
    a8 = Assignment(week=1, name="ex8", duration=Time(h=2), kind=kinds["TASK"])
    a9 = Assignment(week=1, name="ex9", duration=Time(h=1), kind=kinds["TASK"])
    a10 = Assignment(week=1, name="ex10", duration=Time(h=1), kind=kinds["TASK"])
    a11 = Assignment(week=1, name="ex11", duration=Time(h=5), kind=kinds["TASK"])
    """
    a1 = Assignment(week=1, name="ex1", duration=Time(h=1), kind=kinds["TASK"])
    a2 = Assignment(week=1, name="ex2", duration=Time(h=1, m=30), kind=kinds["TASK"])
    a3 = Assignment(week=1, name="ex3", duration=Time(h=3), kind=kinds["TASK"])
    a4 = Assignment(week=1, name="ex4", duration=Time(h=3, m=15), kind=kinds["TASK"])
    a5 = Assignment(week=1, name="ex5", duration=Time(h=2, m=45), kind=kinds["TASK"])
    a6 = Assignment(week=1, name="ex6", duration=Time(h=2), kind=kinds["TASK"])
    a7 = Assignment(week=1, name="ex7", duration=Time(h=1, m=15), kind=kinds["TASK"])
    a8 = Assignment(week=1, name="ex8", duration=Time(h=2, m=15), kind=kinds["TASK"])
    a9 = Assignment(week=1, name="ex9", duration=Time(h=4), kind=kinds["TASK"])
    a10 = Assignment(week=1, name="ex10", duration=Time(h=3, m=45), kind=kinds["TASK"])
    a11 = Assignment(week=1, name="ex11", duration=Time(h=4, m=15), kind=kinds["TASK"])
    """

    c = Constraints()

    ofir = User("Ofir", c)

    ofir.add_assignment(a1)
    ofir.add_assignment(a2)
    ofir.add_assignment(a3)
    ofir.add_assignment(a4)
    ofir.add_assignment(a5)
    ofir.add_assignment(a6)
    ofir.add_assignment(a7)
    ofir.add_assignment(a8)
    ofir.add_assignment(a9)
    ofir.add_assignment(a10)
    ofir.add_assignment(a11)

    ofir.schedule_week(1)

    print(ofir)
    #print(ofir.get_schedule(1))




if __name__ == '__main__':
    main()
