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
