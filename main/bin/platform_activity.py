'''
This module handles data processing for platform activity data

'''

from datetime import datetime, timedelta
from main.models import User
from .helper import check_db_status


def detailed_activity(platform, username):
    """
    Gathers hours spent on a platform over the last 7 days

    :param username
    :param platform: The platform to get data for ('facebook', 'youtube', 'netflix' or 'google')
    :return: Array of hours spent each day *where day7 is today*
    """

    if check_db_status(username) == 1:
        series = [{
            "name": "Could not connect to DB",
            "data": [],
            "visible": True
        }]
        return series

    # Retrieve user:
    person = User.objects.get(username=username)
    summary_stats_arr = person.summary_stats

    # Date of first day this week:
    monday_date = (datetime.today() - timedelta(days=datetime.today().isoweekday() % 7 - 1)).date()

    # Get summary stats for the last week
    # (This assumes that the summary_stat array is in ascending order of dates.)
    weekly_stats = []
    days_with_data = 0

    print(monday_date)
    for day in summary_stats_arr:
        if day.timestamp.date() >= monday_date:
            days_with_data += 1
            weekly_stats.append(day)

    print(weekly_stats)

    if platform == "facebook":
        # Add data into weekly series
        series = [{
            "name": 'Total',
            "data": [],
            "visible": True
        }, {
            "name": 'Messages',
            "data": [],
            "visible": False
        }, {
            "name": 'Posts',
            "data": [],
            "visible": False
        }, {
            "name": 'Comments',
            "data": [],
            "visible": False
        }, {
            "name": 'Likes',
            "data": [],
            "visible": False
        }, {
            "name": 'Groups',
            "data": [],
            "visible": False
        }, {
            "name": 'Others',
            "data": [],
            "visible": False
        }]
    else:
        series = [{
            "name": platform.capitalize(),
            "data": [],
            "visible": True
        }]

    if platform == "youtube":
        for day in weekly_stats:
            series[0]["data"].append(round(day.yt.total_minutes / 60, 1))
    elif platform == "netflix":
        for day in weekly_stats:
            series[0]["data"].append(round(day.netflix.total_minutes / 60, 1))
    elif platform == "google":
        for day in weekly_stats:
            series[0]["data"].append(round(day.google.total_minutes / 60, 1))
    elif platform == "facebook":
        for day in weekly_stats:
            series[0]["data"].append(round(day.fb.total_minutes / 60, 1))
            series[1]["data"].append(round(day.fb.message_minutes / 60, 1))
            series[2]["data"].append(round(day.fb.posts_minutes / 60, 1))
            series[3]["data"].append(round(day.fb.comments_minutes / 60, 1))
            series[4]["data"].append(round(day.fb.likes_minutes / 60, 1))
            series[5]["data"].append(round(day.fb.groups_minutes / 60, 1))
            series[6]["data"].append(round(day.fb.other_minutes / 60, 1))
    else:
        return

    # If there isn't a full week of data, fill the rest to 0.
    for i in range(7 - days_with_data):
        for type in series:
            type["data"].append(0)

    return series
