from django.core.management.base import BaseCommand, CommandError
import os
import shutil
from datetime import datetime, timedelta, time
from django.utils import timezone
import pytz
from django.conf import settings
from .ingest_fb import IngestFacebook
from .scrub_facebook import download_data
from .ingest_other import IngestOther
# from .helper import sync_update
from main.models import User
import zipfile

'''
    This command adds any recent activity to a User's platform data.
    
    Inputs: 
        username
        password
        platform
        action (sync | update)
        days (number of days ago you want to update summary_stats for)
        
    TODO: 
        - Process multiple types of facebook json files
        - Process other types of platform information
        - Utilise a checkpoint file which stores the epoch ts of recently pushed activity
        - Add google data processing
    
'''


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('user_details', nargs='+', type=str)
        # parser.add_argument('days', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        print(kwargs)
        username = kwargs['user_details'][0]
        platform = kwargs['user_details'][1]
        action = kwargs['user_details'][2]
        go_back_days = int(kwargs['user_details'][3])
        # go_back_days = kwargs['days'][0]

        # sync_update(username, password, platform, action, go_back_days)
        if platform == "youtube" or platform == "netflix" or platform == 'google':
            if platform == 'youtube':
                platform_index = 1
            elif platform == "netflix":
                platform_index = 2
            elif platform == 'google':
                platform_index = 3


            current_datetime = timezone.now() - timedelta(days=go_back_days)
            midnight = current_datetime.replace(hour=0, minute=0, second=1, microsecond=0)
            midnight_epoch = midnight.timestamp()

            # Get epoch for end of the day insepcted (11:59:59 pm)
            end_of_day_epoch = midnight_epoch + 86399

            video_platform = IngestOther(username, platform_index)
            if action == "sync":
                video_platform.process_raw(current_datetime.timestamp(), go_back_days)

            elif action == "update":
                video_platform.update_minutes(current_datetime, midnight_epoch)

        # Process facebook data
        if platform == "facebook":
            #######################################################################################################
            #                                 Enter path for facebook directory here                              #
            #######################################################################################################
            download_dir = settings.DEFAULT_DOWNLOAD_PATH
            fb_name = settings.FB_NAME

            fb_username = User.objects.get(username=username).linked_platforms[0].email
            fb_password = User.objects.get(username=username).linked_platforms[0].password

            if not os.access(download_dir, os.R_OK):
                bash_command = "chmod -R 777 " + fb_name
                os.chdir(download_dir)
                os.system(bash_command)

            facebook = IngestFacebook(username, download_dir + 'facebook-' + fb_name)

            if "sync" in action:
                # Download data
                download_data(fb_username, fb_password, download_dir, 1)

                # unzip file
                path_to_zip = settings.DEFAULT_DOWNLOAD_PATH + 'facebook-' + settings.FB_NAME + '.zip'
                directory_to_extract_to =  settings.DEFAULT_DOWNLOAD_PATH + 'facebook-' + settings.FB_NAME
                with zipfile.ZipFile(path_to_zip, 'r') as zip_ref:
                    zip_ref.extractall(directory_to_extract_to)

                # # Push data to MongoDB
                facebook.process_comments()
                facebook.process_messages()
                facebook.process_other()
                facebook. process_likes()
                facebook.process_groups()
                facebook.process_posts()

                # Delete folder and delete zip file.
                try:
                    shutil.rmtree(os.path.expanduser(download_dir + 'facebook-' + fb_name))
                except FileNotFoundError:
                    print("No directory to delete")

                try:
                    os.remove(download_dir + 'facebook-' + fb_name + '.zip')
                except FileNotFoundError:
                    print("nN zip file to delete")

            elif action == "update":
                current_datetime = timezone.now()- timedelta(days=go_back_days)
                current_date = current_datetime.date()
                midnight = current_datetime.replace(hour=0, minute=0, second=1, microsecond=0)
                midnight_epoch = midnight.timestamp()


                # Get epoch for end of the day insepcted (11:59:59 pm)
                end_of_day_epoch = midnight_epoch + 86399
                end_of_date_datetime = datetime.fromtimestamp(end_of_day_epoch)

                # Update
                facebook.update_daily_minutes(current_datetime, midnight_epoch)
