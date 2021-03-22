from main.models import User, Data, SummaryStats, FacebookEntry, YTEntry, NetflixEntry, GoogleEntry
# from django.utils import timezone
# from datetime import datetime
# from django.core.management.base import BaseCommand, CommandError
# import os
# from .ingest_fb import IngestFacebook
# from .scrub_facebook import download_data
# import shutil
# from .ingest_other import IngestOther
from datetime import datetime, timedelta, time
import pytz
from django.utils import timezone


def update_mongo(data_dict, username, platform_index):
    """
    Updates mongoDB user with info about platform activity

    :param platform_index: Index of platform in database (0: fb, 1: yt, 2: nettlix, 3: google)
    :param data_dict: Array of dictionaries containing timestamp of activity, time spent.
    :param username: username
    :return:
    """

    if len(data_dict) == 0:
        return "No events"

    print("username: ", username)

    person = User.objects.get(username=username)

    obj = person.linked_platforms[platform_index]
    obj.last_updated = timezone.now()

    # Append data object with new activity information

    for event in data_dict:
        data_obj = Data()
        data_obj.timestamp_epoch = event["timestamp_epoch"]
        data_obj.raw_data = event["raw_data"]
        data_obj.spent_minutes = event["spent_minutes"]
        obj.data.append(data_obj)

    # Push new data into mongoDB document.
    person.save()



def get_current_summary(person, summary_arr, current_datetime):
    """
    Returns current summary object of user

    :param summary_arr: Array of summaries of user
    :return: summary object
    """

    # Retrieve correct entry in summary_stats array
    today_summary = None
    current_date = current_datetime.date()

    for summary_entry in reversed(summary_arr):
        ts = int(summary_entry.timestamp.strftime("%s"))
        historical_datetime = datetime.fromtimestamp(ts)
        historical_date = historical_datetime.date()


        # Create new entry in array if today's summary doesn't exist yet
        print("current date: ", current_date)
        print("historical date:", historical_date)
        if current_date > historical_date:
            print("creating new entry")
            sp = person.summary_stats

            new_entry = SummaryStats()
            new_entry.timestamp = current_datetime
            new_entry.fb = FacebookEntry()
            new_entry.yt = YTEntry()
            new_entry.netflix = NetflixEntry()
            new_entry.google = GoogleEntry()

            sp.append(new_entry)
            today_summary = new_entry

            break
        elif current_date == historical_date:
            today_summary = summary_entry
            minute_count = summary_entry.yt.total_minutes
            print("prev: ", minute_count)
            break

    return today_summary

#
# def sync_update(username, password, platform, action, go_back_days):
#     if platform == "yt" or platform == "netflix" or platform == 'google':
#         if platform == 'yt':
#             platform_index = 1
#         elif platform == "netflix":
#             platform_index = 2
#         elif platform == 'google':
#             platform_index = 3
#
#         current_datetime = timezone.now() - timedelta(days=go_back_days)
#         midnight = current_datetime.replace(hour=0, minute=0, second=1, microsecond=0)
#         midnight_epoch = midnight.timestamp()
#
#         # Get epoch for end of the day insepcted (11:59:59 pm)
#         end_of_day_epoch = midnight_epoch + 86399
#
#         video_platform = IngestOther(username, password, platform_index)
#         if action == "sync":
#             video_platform.process_raw(current_datetime.timestamp(), 1)
#
#         elif action == "update":
#             video_platform.update_minutes(current_datetime, midnight_epoch)
#
#     # Process facebook data
#     if platform == "fb":
#         #######################################################################################################
#         #                                 Enter path for facebook directory here                              #
#         #######################################################################################################
#         fb_dir = '/Users/jessica.a.wu/Documents/Personal/2019/Semester2/ELEC3609/Assignment/ELEC3609-DJJ' \
#                  '/myData/main/management/commands/'
#
#         # TODO: need to get this manually somehow
#         fb_name = "jess.wu.756"
#
#         if not os.access(fb_dir, os.R_OK):
#             bash_command = "chmod -R 777 " + fb_name
#             os.chdir(fb_dir)
#             os.system(bash_command)
#
#         facebook = IngestFacebook(username, 'fb', fb_dir + fb_name)
#
#         if "sync" in action:
#             # Download data
#
#             download_dir = "/Users/jessica.a.wu/Downloads"
#             download_data('<username>', '<pw>', download_dir, 1)
#
#             # Push data to MongoDB
#             facebook.process_comments()
#             facebook.process_messages()
#             facebook.process_other()
#             facebook.process_likes()
#             facebook.process_groups()
#             facebook.process_posts()
#
#             # TODO: Delete folder and zip file.
#             # shutil.rmtree(os.path.expanduser(download_dir))
#
#         elif action == "update":
#             current_datetime = timezone.now() - timedelta(days=go_back_days)
#             current_date = current_datetime.date()
#             midnight = current_datetime.replace(hour=0, minute=0, second=1, microsecond=0)
#             midnight_epoch = midnight.timestamp()
#
#             # Get epoch for end of the day insepcted (11:59:59 pm)
#             end_of_day_epoch = midnight_epoch + 86399
#             end_of_date_datetime = datetime.fromtimestamp(end_of_day_epoch)
#
#             # Update
#             facebook.update_daily_minutes(current_datetime, midnight_epoch)
