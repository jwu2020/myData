from main.models import User


class Platform:

    def __init__(self, username, platform_index):
        self.username = username
        self.platform_index = platform_index
        self.person = User.objects.get(username=username)

    def get_link(self):
        """
        Find out whether user is linked to a platform

        :param self.username: (str)  self.username/email of user
        :param self.platform_index: (int) determines platform [0: fb, 1: yt, 2: netflix, 3: google]
        :return: (bool) Whether a user is linked to a platform
        """
        # Get goal value and return
        link = self.person.linked_platforms[self.platform_index].link

        if not link:
            return 1
        else:
            return 0

    def get_goal(self):
        """
        Returns max number of hours spend on a platform that the user has set for themselves

        :param self.username: (str) self.username/email of user
        :param self.platform_index: (int) determines platform [0: fb, 1: yt, 2: netflix, 3: google]
        :return: (int) Number of hours that user has set as limit
        """

        # Get goal value and return
        goal = self.person.linked_platforms[self.platform_index].goal

        return goal

    def update_link(self, action, username=None, password=None):
        """
        Updated linking field and platform login details in backend.
        This is called in views.py.

        :param username: email of platform the user is linking to
        :param password: password of platform user is linking to.
        :param self.username: (str) self.username/email of user
        :param self.platform_index: (int) Determines platform that will be linked/unlinked
        :param action: (str) Link ("link") or unlinking ("unlink") action
        :return: None
        """

        # Retrieve User object
        platform_obj = self.person.linked_platforms[self.platform_index]
        platform_obj.email = username
        platform_obj.password = password

        # Update platform link field and save
        if action == "link":
            platform_obj.link = True
        else:
            platform_obj.link = False

        self.person.save()

    def update_goal(self, goal_val):
        """
        Updates the user's platform goal (max time they can spend on a platform)

        :param self.username: self.username / email of user
        :param self.platform_index: Determines platform to update [0: fb, 1: yt, 2: netflix, 3: google]
        :param goal_val: Value to new goal
        :return: None
        """

        # Update and save person
        platform_obj = self.person.linked_platforms[self.platform_index]
        platform_obj.goal = goal_val
        self.person.save()
