from user import User


class Manager:
    def __init__(self):
        self.__users = []

    def get_users(self):
        return self.__users

    def add_user(self, user: User):
        self.__users.append(user)

    def del_user(self, user: User):
        if user in self.__users:
            self.__users.remove(user)

    def schedule_week(self, week):
        # TODO: implement this using forward checking
        pass

    def schedule_week(self, week: int, user: User):
        """
        schedule the tasks of a specific user in specific week
        takes all of the assignments in user and sets for them a day and an houer
        """
        user.schedule_week(week)
