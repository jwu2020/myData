"""
This module contains functions which handle notification processing.

"""
import datetime
from mongoengine import DoesNotExist
from main.models import User


def check(username):
    """
    :param username
    :return: JSON with the time_spent and goal for each platform for today.
    """

    # retrieve the user
    try:
        person = User.objects.get(username=username)
    except DoesNotExist:
        return None

    # check each platform if the time spent has exceeded the goal
    linked_platforms = person.linked_platforms
    summary_stats_arr = person.summary_stats
    date_today = datetime.date.today()

    summary_stats_today = None
    for daily_entry in reversed(summary_stats_arr):
        if daily_entry.timestamp.date() == date_today:
            summary_stats_today = daily_entry
            break

    if summary_stats_today is None:
        return None

    alert = []
    for index in range(len(linked_platforms)):
        platform = linked_platforms[index]
        goal = platform.goal

        if platform.platform == 'fb':
            if goal <= summary_stats_today.fb.total_minutes/60:
                alert.append('Facebook')

        elif platform.platform == 'yt':
            if goal <= summary_stats_today.fb.total_minutes/60:
                alert.append('Youtube')

        elif platform.platform == 'netflix':
            if goal <= summary_stats_today.fb.total_minutes/60:
                alert.append('Netflix')

        elif platform.platform == 'google':
            if goal <= summary_stats_today.fb.total_minutes/60:
                alert.append('Google')

    data_json = {'platform': alert}
    print('data_json:', data_json)

    return data_json