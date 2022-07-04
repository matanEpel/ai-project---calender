
class Time:

    def __init__(self, h=0, m=0):
        if h < 0 or h > 24 or m < 0 or m >= 59:
            raise ValueError("hours or minutes are not in range")
        self.hours = h
        self.minutes = m

    def get_hours(self):
        return self.hours

    def get_minutes(self):
        return self.minutes

    def set_minutes(self, m):
        self.minutes = m

    def set_hours(self, h):
        self.hours = h

    def __add__(self, other):
        hours = self.get_hours() + other.get_hours()
        minutes = self.get_minutes() + other.get_minutes()
        q, r = divmod(minutes, 60)
        return Time(hours + q, r)

    def __iadd__(self, other):
        hours = self.get_hours() + other.get_hours()
        minutes = self.get_minutes() + other.get_minutes()
        q, r = divmod(minutes, 60)
        self.set_hours(hours + q)
        self.set_minutes(r)

    def __eq__(self, other):
        """
            define the operator ==
        """
        return self.get_hours() == other.get_hours() and self.get_minutes() == other.get_minutes()

    def __lt__(self, other):
        """
            define the operator <
        """
        if self.get_hours() < other.get_hours():
            return True

        if self.get_hours() > other.get_hours():
            return False

        if self.get_minutes() < other.get_minutes():
            return True

        if self.get_minutes() > other.get_minutes():
            return False

        # if arrived here, they are equals
        return False

    def __le__(self, other):
        """
            define the operator <=
        """
        if self == other:
            return True

        return self < other

    def __str__(self):
        return "{}:{}".format(self.hours, self.minutes)

    @staticmethod
    def is_overlap(x1, x2, y1, y2):
        """
            checks if the the 2 intervals [x1, x2] and [y1, y2] are overlapping
        """
        return x1 <= y2 and y1 <= x2


