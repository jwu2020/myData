from datetime import datetime, timedelta
import pytz
from main.models import User
from .helper import check_db_status



def get_bar_chart(username):
    """
    Calculate the amount of time spend on each social media platform today.

    :type username: object Username
    :return: Array with each element assigned to each platform.
            Each element stores the amount of activity calculated.
            2nd element includes status of database (Disconnected(1) or connected(0))
    """

    if check_db_status(username) == 1:
        data = [{
            'name': 'Facebook',
            'y': 0,
        }, {
            'name': 'Youtube',
            'y': 0
        }, {
            'name': 'Netflix',
            'y': 0
        }, {
            'name': 'Google',
            'y': 0
        }]
        return data

    person = User.objects.get(username=username)
    summary_stats_arr = person.summary_stats
    platform_details = person.linked_platforms

    # Retrieve today's statistics
    tz = pytz.timezone("Australia/Sydney")
    today = datetime.now(tz).date()
    today_stats = None

    for daily_entry in reversed(summary_stats_arr):
        print("entries date: ", daily_entry.timestamp.date())
        if daily_entry.timestamp.date() == today:
            today_stats = daily_entry

    # Return today's summary
    if today_stats is None:
        data = [{
            'name': 'Facebook',
            'y': 0,
        }, {
            'name': 'Youtube',
            'y': 0
        }, {
            'name': 'Netflix',
            'y': 0
        }, {
            'name': 'Google',
            'y': 0
        }]
    else:
        data = [{
            'name': 'Facebook',
            'y': round(today_stats.fb.total_minutes/60, 1),
        }, {
            'name': 'Youtube',
            'y': round(today_stats.yt.total_minutes/60, 1)
        }, {
            'name': 'Netflix',
            'y': round(today_stats.netflix.total_minutes/60, 1)
        }, {
            'name': 'Google',
            'y': round(today_stats.google.total_minutes/60, 1)
        }]

    print('data: ', data)
    # Only return data for platforms that have been enabled.
    enabled_data = []
    data_index = 0
    for platform in platform_details:
        if platform.link:
            enabled_data.append(data[data_index])

        data_index += 1

    return enabled_data


def get_count(array, timestamp_var, start_epoch, end_epoch):
    """
    Calculates the number events that take space between specified time period.

    :param array: Array timestamps
    :param timestamp_var: name of timestamp field
    :param start_epoch: start timestamp
    :param end_epoch: end timestamp
    :return: Int number of events between start and end epoch time.
    """

    count = 0

    for event in array:
        if (event[timestamp_var] < start_epoch) or (event[timestamp_var] > end_epoch):
            break

        count += 1

    return count


def get_categories(scope):
    """
    Sets the x variables

    :param scope: Values of the y axis
    :return: array.
    """

    if scope == 'day':
        return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    if scope == "month":
        arr = []
        for i in range(12):
            arr.append(i + 1)
        return arr


def get_time_chart(username):
    """

    :return: Array containing objects for each activity.
        In each activity object, there is an array with aggregated
        time for each time bucket. 2nd element includes status of
        database (Disconnected(1) or connected(0))
    """
    # Retrieve user:
    if check_db_status(username) == 1:
        series = [{
            "name": 'Facebook',
            "data": []
        }, {
            "name": 'Youtube',
            "data": []
        }, {
            "name": 'Netflix',
            "data": []
        }, {
            "name": 'Google',
            "data": []
        }]

        return series

    person = User.objects.get(username=username)
    summary_stats_arr = person.summary_stats
    platform_details = person.linked_platforms

    # Date of first day this week:
    # monday: today - 1
    # tuesday: today -
    monday_date = (datetime.today() - timedelta(days=(datetime.today().isoweekday()) - 1)).date()
    today_date = datetime.today()

    print("monday_date: ", monday_date)
    print("today_date: ", today_date)

    # Get summary stats for the last week
    # (This assumes that the summary_stat array is in ascending order of dates.)
    weekly_stats = []

    for day in summary_stats_arr:
        if day.timestamp.date() < monday_date:
            continue

        weekly_stats.append(day)

    # Add data into weekly series
    series = [{
        "name": 'Facebook',
        "data": []
    }, {
        "name": 'Youtube',
        "data": []
    }, {
        "name": 'Netflix',
        "data": []
    }, {
        "name": 'Google',
        "data": []
    }]

    for day in weekly_stats:
        print(day.timestamp)
        series[0]["data"].append(round(day.fb.total_minutes/60, 1))
        series[1]["data"].append(round(day.yt.total_minutes/60, 1))
        series[2]["data"].append(round(day.netflix.total_minutes/60, 1))
        series[3]["data"].append(round(day.google.total_minutes/60, 1))

    # If there isn't a full week of data, fill the rest to 0.
    print(len(weekly_stats))

    remaining_days = 7 - len(weekly_stats)
    print("adding ", remaining_days, " to arr")
    for i in range(remaining_days):
        series[0]["data"].append(0.0)
        series[1]["data"].append(0.0)
        series[2]["data"].append(0.0)
        series[3]["data"].append(0.0)

    print(series)

    # Only return data for platforms that have been enabled.
    enabled_data = []
    data_index = 0
    for platform in platform_details:
        if platform.link:
            enabled_data.append(series[data_index])
        data_index += 1

    # Assuming scope is daily
    return enabled_data