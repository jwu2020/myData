import json
from main.models import User, Data
import glob
import os
from django.utils import timezone
from .helper import get_current_summary


class IngestFacebook(object):
    def __init__(self, username, fb_dir):
        self.username = username
        self.fb_home = fb_dir

    def update_mongo(self, timestamp_arr, activity_type):
        """
        Pushes new facebook activity information to main mongoDB

        :param timestamp_arr: Array with timestamps which represent when activity was recorded
        :param activity_type: fb activity type
        :return: None
        """
        if len(timestamp_arr) == 0:
            return "No events for: ", activity_type

        # # Find data object field in main - this will be edited.
        person = User.objects.get(username=self.username)
        obj = person.linked_platforms[0]

        # tz = pytz.timezone("Australia/Sydney")
        # current_date_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
        # current_datetime = current_date_utc.astimezone(pytz.timezone("Australia/Sydney"))

        current_datetime = timezone.now()

        obj.last_updated = timezone.now()
        # Append data object with new activity information

        for ts in timestamp_arr:
            data_obj = Data()
            data_obj.timestamp_epoch = ts
            data_obj.raw_data = activity_type.title()
            data_obj.spent_minutes = float(1)
            obj.data.append(data_obj)

        # Push new data into mongoDB document.
        person.save()

    def process_messages(self):
        """
        Processes messagess json file and pushes these activities to the mongoDB

        :return: None
        """

        # Get list of folder names for each person
        try:
            os.chdir(self.fb_home + '/messages/inbox/')
        except FileNotFoundError:
            print("no messages")
            return

        person_folder = []
        for folder_name in glob.glob("*"):
            person_folder.append(folder_name)

        ts_arr = []
        activity_type = 'messages'

        # For each person, access message_1.json and append timestamp/activity to ts_arr
        for name in person_folder:

            filename = self.fb_home + '/messages/inbox/' + name + '/message_1.json'
            if (check_files([filename])) == -1:
                return -1

            with open(filename, 'r') as message_f:
                message_j = json.load(message_f)

            # Store all timestamps of new activities
            for activity in message_j[activity_type]:
                ts = activity['timestamp_ms'] / 1000
                ts_arr.append(ts)

        self.update_mongo(ts_arr, 'Messages')

    def process_comments(self):
        """
        Processes comments json file and pushes these activities to the mongoDB

        :return: None
        """

        # Load in json data
        filename = self.fb_home + '/comments/comments.json'

        if (check_files([filename])) == -1: return -1

        with open(filename, 'r') as j:
            loaded_j = json.load(j)

        # Store all timestamps of new activities
        activity_type = list(loaded_j.keys())[0]
        ts_arr = []

        for activity in loaded_j[activity_type]:
            ts_arr.append(activity['timestamp'])

        # Update MongoDB
        self.update_mongo(ts_arr, activity_type)

    def process_other(self):
        """
        Processes other_activity json file and pushes these activities to the mongoDB

        :return: None
        """

        # Load in json data
        f1 = self.fb_home + '/other_activity/pokes.json'
        f2 = self.fb_home + '/other_activity/polls_you_voted_on.json'

        # Store all timestamps of new activities
        ts_arr = []

        if check_files([f1]) == 0:
            with open(f1, 'r') as pokes_f:
                pokes_j = json.load(pokes_f)
                pokes_activity_type = list(pokes_j.keys())[0]

            for activity in pokes_j[pokes_activity_type]['data']:
                ts_arr.append(activity['timestamp'])

        if check_files([f2]) == 0:
            with open(f2, 'r') as polls_f:
                polls_j = json.load(polls_f)
                polls_activity_type = list(polls_j.keys())[0]

            for activity in polls_j[polls_activity_type]:
                ts_arr.append(activity['timestamp'])

        # Update MongoDB
        self.update_mongo(ts_arr, 'Other activity')

    def process_likes(self):
        """
        Processes comment json file and pushes these activities to the mongoDB

        :return: None
        """

        # Load in json data and activity types
        f1 = self.fb_home + '/likes_and_reactions/likes_on_external_sites.json'
        f2 = self.fb_home + '/likes_and_reactions/pages.json'
        f3 = self.fb_home + '/likes_and_reactions/posts_and_comments.json'

        # Store all timestamps of new activities
        ts_arr = []

        if check_files([f1]) == 0:
            with open(f1, 'r') as external_f:
                external_j = json.load(external_f)
            external_activity_type = list(external_j.keys())[0]

            for activity in external_j[external_activity_type]:
                ts_arr.append(activity['timestamp'])

        if check_files([f2]) == 0:
            with open(f2, 'r') as pages_f:
                pages_j = json.load(pages_f)
            pages_activity_type = "page_likes"

            for activity in pages_j[pages_activity_type]:
                ts_arr.append(activity['timestamp'])

        if check_files([f3]) == 0:
            with open(f3, 'r') as posts_f:
                posts_j = json.load(posts_f)
            posts_activity_type = "reactions"

            for activity in posts_j[posts_activity_type]:
                ts_arr.append(activity['timestamp'])

        self.update_mongo(ts_arr, "Likes and Reactions")

    def process_groups(self):
        """
        Processes groups json file and pushes these activities to the mongoDB

        :return: None
        """

        # Load in json data of group membership json files

        f1 = self.fb_home + '/groups/your_group_membership_activity.json'
        f2 = self.fb_home + '/groups/your_posts_and_comments_in_groups.json'

        # Store all timestamps of new activities
        ts_arr = []

        if check_files([f1]) == 0:
            with open(f1, 'r') as posts_comments_f:
                posts_comments_j = json.load(posts_comments_f)

            post_activity_type = list(posts_comments_j.keys())[0]
            for activity in posts_comments_j[post_activity_type]:
                ts_arr.append(activity['timestamp'])

        if check_files([f2]) == 0:
            with open(f2, 'r') as groups_f:
                groups_f = json.load(groups_f)

            # Store all timestamps of new activities
            group_activity_type = list(groups_f.keys())[0]
            for activity in groups_f[group_activity_type]["activity_log_data"]:
                ts_arr.append(activity['timestamp'])

        # Push data to mongoDB
        self.update_mongo(ts_arr, 'groups')

    def process_posts(self):
        """
        Processes posts json file and pushes these activities to the mongoDB

        :return: None
        """

        # Load in json data
        f1 = self.fb_home + '/posts/your_posts_1.json'

        if (check_files([f1])) == -1: return -1

        with open(f1, 'r') as posts_f:
            posts_j = json.load(posts_f)

        # Store all timestamps of new activities
        ts_arr = []

        for activity in posts_j:
            ts_arr.append(activity['timestamp'])

        # Update MongoDB
        self.update_mongo(ts_arr, 'Posts')

    # def update_minutes(self):
    #     """
    #
    #
    #     :param start:
    #     :param end:
    #     :return:
    #     """
    #     current_date_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
    #     current_datetime = current_date_utc.astimezone(pytz.timezone("Australia/Sydney"))
    #     current_date = current_datetime.date() - timedelta(days=1)
    #
    #     # tz = pytz.timezone("Australia/Sydney")
    #     midnight = datetime.combine(current_date, time(0, 0))
    #     # midnight = tz.localize(datetime.combine(current_date, time(0, 0)), is_dst=None)
    #     midnight_epoch = midnight.astimezone(pytz.timezone("Australia/Sydney")).timestamp()
    #
    #     end_of_day_epoch = midnight_epoch + 86399
    #
    #     #    number of seconds in 1 day: 86,399
    #
    #     self.update_daily_minutes(current_datetime, midnight_epoch)

    def update_daily_minutes(self, current_datetime, midnight_epoch):
        """
        Updates facebook summary with calculated events for each facebook activity.

        :param current_datetime: last timestamp that we will inspect for activities
        :param midnight_epoch: earliest timestamp that we will inspect for activities (midnight of day of current_datetime)
        :return: None
        """

        current_date = current_datetime.date()
        now_epoch = current_datetime

        ###########################################################################################
        #                               Get current summary_stats object                          #
        ###########################################################################################

        # Retrieve the user object from MongoDB
        person = User.objects.get(username=self.username)
        summary_arr = person.summary_stats

        # Retrieve correct entry in summary_stats array
        today_summary = get_current_summary(person, summary_arr, current_datetime)

        ###########################################################################################
        #                                     Get activity count                                  #
        ###########################################################################################

        # Get all fb data
        all_data = person.linked_platforms[0].data

        # Get activity counts for each activity
        activity_counts = {"Messages": 0, "Posts": 0, "Comments": 0, "Groups": 0, "Likes And Reactions": 0,
                           "Other Activity": 0}

        for event in reversed(all_data):
            if (event.timestamp_epoch is None) or (
                    (event.timestamp_epoch < midnight_epoch) or (event.timestamp_epoch > now_epoch.timestamp())):
                continue

            activity_counts[str(event.raw_data)] += 1

        # Get count for each activity of today
        today_summary.fb.message_minutes = activity_counts["Messages"]
        today_summary.fb.posts_minutes = activity_counts["Posts"]
        today_summary.fb.comments_minutes = activity_counts["Comments"]
        today_summary.fb.likes_minutes = activity_counts["Likes And Reactions"]
        today_summary.fb.groups_minutes = activity_counts["Groups"]
        today_summary.fb.other_minutes = activity_counts["Other Activity"]
        today_summary.fb.total_minutes = activity_counts["Messages"] + activity_counts["Posts"] \
                                         + activity_counts["Comments"] + activity_counts["Likes And Reactions"] \
                                         + activity_counts["Groups"] + activity_counts["Other Activity"]

        for key, value in activity_counts.items():
            print(key, ":", value)

        # Push to MongoDB
        person.save()


def check_files(file_arr):
    """
    Checks the existence of multiple files.

    :param file_arr: Array of file names to check the existence of
    :return: 0: files exist. -1: One or more files don't exist.
    """

    for filename in file_arr:
        if not os.path.isfile(filename):
            print('Cannot find: ' + filename + ". No data found in this poll")
            return -1

    return 0
