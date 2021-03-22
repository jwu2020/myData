from decimal import Decimal
import json
from django.conf import settings
from main.models import User
from .scrub_youtube import download_youtube_data
from .scrub_netflix import download_netflix_data
from .scrub_google import download_google_data
from .helper import update_mongo, get_current_summary


class IngestOther:
    def __init__(self, username, platform_index):
        self.username = username
        self.platform_index = platform_index

    def update_minutes(self, current_datetime, midnight_epoch):
        """
         Updates facebook summary with calculated events for each facebook activity.
         This will run every day.

        :param current_datetime: Current timestamp
        :param midnight_epoch: Timestamp of midnight of current day
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
        minute_count = 0.0
        today_summary = get_current_summary(person, summary_arr, current_datetime)

        ###########################################################################################
        #                                     Get activity count                                  #
        ###########################################################################################

        # Get data for today
        all_data = person.linked_platforms[self.platform_index].data

        # Get activity counts for each activity
        for event in reversed(all_data):
            if (event.timestamp_epoch is None) or (
                    (event.timestamp_epoch < midnight_epoch) or (event.timestamp_epoch > now_epoch.timestamp())):
                continue
            print("Adding: ", event.spent_minutes)
            minute_count += event.spent_minutes

        # Get count for each activity of today
        if self.platform_index == 1:
            today_summary.yt.total_minutes += minute_count
        elif self.platform_index == 2:
            today_summary.netflix.total_minutes += minute_count
        elif self.platform_index == 3:
            today_summary.google.total_minutes += minute_count

        print("total min today = ", minute_count)

        # Push to MongoDB
        person.save()

    def process_raw(self, now_epoch, day_range):
        """

        :param now_epoch: Current timestamp in epoch format
        :param day_range: Range of days (between now and x days ago) that the script will srub data from.
        :return: json
        """
        day_range = 2
        # Download data
        if self.platform_index == 1:
            youtube_username = User.objects.get(username=self.username).linked_platforms[1].email
            youtube_password = User.objects.get(username=self.username).linked_platforms[1].password
            raw_json = json.loads(download_youtube_data(youtube_username, youtube_password, day_range))
        elif self.platform_index == 2:
            netflix_username = User.objects.get(username=self.username).linked_platforms[2].email
            netflix_password = User.objects.get(username=self.username).linked_platforms[2].password
            netflix_name = settings.NETFLIX_NAME
            raw_json = json.loads(download_netflix_data(netflix_username, netflix_password, day_range, netflix_name))
        elif self.platform_index == 3:
            google_username = User.objects.get(username=self.username).linked_platforms[3].email
            google_password = User.objects.get(username=self.username).linked_platforms[3].password
            print(google_username, google_password)
            raw_json = json.loads(download_google_data(google_username, google_password, day_range))

        # raw_json = {
        #     "date_string1": [
        #         {
        #             "index": 0,
        #             "length": "2:31",
        #             "watched": "width: 10%;"
        #         }
        #     ],
        #     "date_string2": [
        #         {
        #             "index": 0,
        #             "length": "2:31",
        #             "watched": "width: 33%;"
        #         },
        #         {
        #             "index": 1,
        #             "length": "12:01",
        #             "watched": "width: 10%;"
        #         }
        #     ]
        # }

        # Convert date_string to epoch
        date_list = raw_json.keys()

        # Calculate spent_minutes for each videos
        sanitize_arr = []

        if self.platform_index < 3:
            for day in date_list:
                daily_list = raw_json[day]

                for video in daily_list:
                    time_spent = float(string_to_minutes(video["length"]) * string_to_percentage(video["watched"]))
                    raw_data = video["index"]

                    # TODO: Change this to the actual timestamp once we can get data for this
                    obj = {"raw_data": raw_data, "spent_minutes": Decimal(time_spent), "timestamp_epoch": now_epoch}
                    sanitize_arr.append(obj)
        else:
            for day in date_list:
                daily_list = raw_json[day]

                for entry in daily_list:
                    hits = entry['hits']

                    obj = {"raw_data": hits, "spent_minutes": hits * 1, "timestamp_epoch": now_epoch}
                    print(obj)
                    sanitize_arr.append(obj)

        # Make changes to mongoDB
        # Make changes to mongoDB
        update_mongo(sanitize_arr, self.username, self.platform_index)


def time_to_datetime(raw_str, current_date):
    """
    Converts string with time to datetime.

    :param raw_str: string time in format "hh:mm am/pm"
    :param current_date: datetime format
    :return: datetime object
    """

    hour_str = raw_str.split(":")[0]
    minutes_str = (raw_str.split(":")[1])[0:2]
    meridiem_str = (raw_str.split(":")[1])[2:]

    hour = int(hour_str)
    min = int(minutes_str)
    if meridiem_str == "PM":
        hour_str = int(hour_str) + 12

    



def string_to_percentage(raw_str):
    """
    Converts string format of css ("width: 10%;") to percentage

    :param raw_str: string format of css ("width: 10%;")
    :return: percentage
    """

    percentage = int(raw_str.split(": ")[1].split("%")[0]) / 100

    return percentage


def string_to_minutes(raw_str):
    """
    Converts time in string format (mm:ss) to number of total minutes.

    :param raw_str:  string format (mm:ss)
    :return:
    """
    print(raw_str)
    str_arr = raw_str.split(":")
    print(str_arr)

    # Dealing with under hour
    if len(str_arr) == 2:
        minute1 = int(str_arr[0])
        minute2 = int(str_arr[1]) / 60
        print(minute1, " + ", minute2)
        total_minutes = minute1 + minute2
    # Dealing with videos over an hour
    else:
        minute1 = int(str_arr[0]) * 60
        minute2 = int(str_arr[0])
        minute3 = int(str_arr[1]) / 60
        total_minutes = minute1 + minute2 + minute3

    return total_minutes
