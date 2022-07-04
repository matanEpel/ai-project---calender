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

    c = Constraints()

    ofir = User("Ofir", c)

    ofir.add_assignment(a1)
    ofir.add_assignment(a2)
    ofir.add_assignment(a3)

    ofir.schedule_week(1)

    print(ofir)
    #print(ofir.get_schedule(1))




if __name__ == '__main__':
    main()
