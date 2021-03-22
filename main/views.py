from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from mongoengine import DoesNotExist
from main.bin.overview import get_bar_chart, get_time_chart, check_db_status
from main.bin.forms.platform import Platform
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from main.bin.platform_activity import detailed_activity
import csv
from django.utils.encoding import smart_str
from main.models import User as UserData
from main.bin.forms.add_user import add_user
from main.bin.notifications_check import check as check_notification
from django.core import management

# Placeholder. Lists users of the platform.
def index(request):
    user_list = UserData.objects.all()
    output = ', '.join([u.username for u in user_list])
    return HttpResponse(output)


def __getindex__(name):
    if name == 'facebook':
        return 0
    elif name == 'youtube':
        return 1
    elif name == 'netflix':
        return 2
    else:
        return 3

def __getgoal__(username):
    goal_list = {
        'facebook': Platform(username, 0).get_goal(),
        'youtube': Platform(username, 1).get_goal(),
        'netflix': Platform(username, 2).get_goal(),
        'google': Platform(username, 3).get_goal(),
    }

    return goal_list

@login_required(login_url='/login')
def poll(request):
    """
    Trigger scrub, sync and update python script for specified platform. Trigger scheduling.
    :param request:
    :return: bool (success or no success)
    """
    # get platform username and password
    username = request.user.username
    platform = request.GET['platform']
    person = User.objects.get(username=username)

    platform_index = None

    if platform == 'facebook':
        platform_index = 0
    elif platform == 'youtube':
        platform_index = 1
    elif platform == 'netflix':
        platform_index = 2
        # netflix_name = request.GET('netflix_name')
    elif platform == 'google':
        platform_index = 3

    management.call_command('process_data', username, platform, 'sync', '0')
    management.call_command('process_data', username, platform, 'update', '0')

    return JsonResponse({'result': 'started polling'})



@login_required(login_url='/login')
def check_notifications(request):
    """
    Poll for notifications

    :param request: Javscript payload
    :return: json dict listing platforms where daily limit has been exceeded.
    """
    username = request.user.username

    notification_list = check_notification(username)

    print(notification_list)
    print(type(notification_list))

    return JsonResponse(notification_list)

@login_required(login_url='/login')
def update_goal(request):
    username = request.user.username
    platform = request.GET['platform']
    goal_val = request.GET['goal']

    Platform(username, __getindex__(platform)).update_goal(goal_val)

    confirm_goal = Platform(username, __getindex__(platform)).get_goal()
    if str(confirm_goal) == goal_val:
        return JsonResponse({'result': 'success'})
    else:
        return JsonResponse({'result': 'error'})

@login_required(login_url='/login')
def disconnect(request):
    username = request.user.username
    platform = request.GET['platform']
    platform_email = ""
    platform_password = ""
    Platform(username, __getindex__(platform)).update_link('unlink', platform_email, platform_password)
    result = Platform(username, __getindex__(platform)).get_link()

    if result == 1:
        return JsonResponse({'result': 'Attempt to disconnect succeeded'})
    else:
        return JsonResponse({'result': 'Attempt to disconnect failed'})

@login_required(login_url='/login')
def connect(request):
    username = request.user.username
    platform = request.GET['platform']
    print(platform)
    platform_email = request.GET['platform_email']
    platform_password = request.GET['platform_password']

    Platform(username, __getindex__(platform)).update_link('link', platform_email, platform_password)
    result = Platform(username, __getindex__(platform)).get_link()

    if result == 0:
        return JsonResponse({'result': 'Attempt to connect succeeded'})
    else:
        return JsonResponse({'result': 'Attempt to connect failed'})


class Login(TemplateView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        result = json.loads(request.body.decode('utf-8'))['value']
        if result['type'] == 'login':
            try:
                user = authenticate(username=result['username'], password=result['password'])
            except Exception as e:
                print(e)
                return JsonResponse({'login': 'error'})

            if user is not None:
                login(request, user)
                return JsonResponse({'login': 'true'})
            else:
                return JsonResponse({'login': 'false'})

        elif result['type'] == 'sign-up':
            try:
                user = User.objects.create_user(result['username'], result['email'], result['password'])

                # Link up user created to the user in the main_user db
                add_user(result['username'], result['password'])
                login(request, user)
            except Exception as e:
                print(e)
                return JsonResponse({'sign-in': 'existing user'})
            return JsonResponse({'sign-in': 'true'})



def logMeOut(request):
    result = json.loads(request.body.decode('utf-8'))['value']
    if result['type'] == 'logout':
        logout(request)
        return JsonResponse({'logout': 'true'})
    return JsonResponse({'logout': 'false'})


@login_required(login_url='/login')
def main(request):
    username = request.user.username
    bar_categories = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pie_data = get_bar_chart(username)
    bar_data = get_time_chart(username)
    db_status = check_db_status(username)

    context = {
        # 'username': username,
        'pie_data': json.dumps(pie_data),
        'bar_data': json.dumps(bar_data),
        'db_status': db_status,
        'bar_categories': json.dumps(bar_categories),
    }
    return render(request, 'main.html', context=context)


def register(request):
    return render(request, 'register.html')

@login_required(login_url='/login')
def goals(request):
    username = request.user.username

    # Checks if it can connect to database
    db_status = check_db_status(username)
    if db_status == 1:
        linked_options = {
            'facebook': 1,
            'youtube': 1,
            'netflix': 1,
            'google': 1,
        }
    else:
        #  Check what accounts are connected
        linked_options = {
            'facebook': Platform(username, 0).get_link(),
            'youtube': Platform(username, 1).get_link(),
            'netflix': Platform(username, 2).get_link(),
            'google': Platform(username, 3).get_link(),
        }

    context = {
        'linked_options': json.dumps(linked_options),
        'goal_list': json.dumps(__getgoal__(username)),
        'username': username
    }

    return render(request, 'goals.html', context=context)

@login_required(login_url='/login')
def accounts(request):
    username = request.user.username

    # Checks if it can connect to database
    db_status = check_db_status(username)
    if db_status == 1:
        linked_options = {
            'facebook': 1,
            'youtube': 1,
            'netflix': 1,
            'google': 1,
        }
    else:
        #  Check what accounts are connected
        linked_options = {
            'facebook': Platform(username, 0).get_link(),
            'youtube': Platform(username, 1).get_link(),
            'netflix': Platform(username, 2).get_link(),
            'google': Platform(username, 3).get_link(),
          }

    context = {
        'linked_options': json.dumps(linked_options)
    }

    return render(request, 'accounts.html', context=context)



@login_required(login_url='/login')
def detailed_netflix(request):
    '''
    Send json for specific Netflix summary

    :param request: Request object
    :return: None
    '''
    username = request.user.username

    # Check if this view is enabled..
    # Only return data for platforms that have been enabled.
    link = Platform(username, 2).get_link()

    if link == 0:
        context = {
            'line_data': json.dumps(detailed_activity('netflix', username)),
            'x_labels': json.dumps(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
            'title': 'Netflix',
            'db_status': check_db_status(username)
        }

        return render(request, 'detailed.html', context=context)
    else:
        context = {'platform': 'Netflix'}
        return render(request, 'unlinked.html', context=context)

@login_required(login_url='/login')
def detailed_google(request):
    '''
    Send json for specific Google summary

    :param request: Request object
    :return: None
    '''
    username = request.user.username

    # Check if this view is enabled..
    # Only return data for platforms that have been enabled.
    link = Platform(username, 3).get_link()

    if link == 0:
        context = {
            'line_data': json.dumps(detailed_activity('google', username)),
            'x_labels': json.dumps(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
            'title': 'Google',
            'db_status': check_db_status(username)
        }
        return render(request, 'detailed.html', context=context)

    else:
        context = {'platform': 'Google'}
        return render(request, 'unlinked.html', context=context)

@login_required(login_url='/login')
def detailed_yt(request):
    '''
    Send json for specific youtube summary

    :param request: Request object
    :return: None
    '''
    username = request.user.username
    # Check if this view is enabled..
    # Only return data for platforms that have been enabled.
    link = Platform(username, 1).get_link()

    if link == 0:
        context = {
            'line_data': json.dumps(detailed_activity('youtube', username)),
            'x_labels': json.dumps(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
            'title': 'Youtube',
            'db_status': check_db_status(username)
        }
        return render(request, 'detailed.html', context=context)
    else:
        context = {'platform': 'Youtube'}
        return render(request, 'unlinked.html', context=context)

@login_required(login_url='/login')
def detailed_fb(request):
    '''
    Send json for specific Facebook summary

    :param request: Request object
    :return: None
    '''

    username = request.user.username

    # Check if this view is enabled..
    # Only return data for platforms that have been enabled.
    link = Platform(username, 0).get_link()

    if link == 0:
        context = {
            'line_data': json.dumps(detailed_activity('facebook', 'j')),
            'x_labels': json.dumps(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
            'title': 'Facebook',
            'db_status': check_db_status(username)
        }
        return render(request, 'detailed.html', context=context)

    else:
        context = {'platform': 'Facebook'}
        return render(request, 'unlinked.html', context=context)


@login_required(login_url='/login')
def download(request):
    """
    Downloads all data for user. Called from main.js.

    :param request: payload containing username
    :return: HTTP response
    """

    username = request.user.username

    # retrieve the user
    try:
        person = UserData.objects.get(username=username)
    except DoesNotExist as e:
        print(e)
        return

    # response content type
    response = HttpResponse(content_type='text/csv')

    # decide the file name
    response['Content-Disposition'] = 'attachment; filename="MyDatata.csv"'

    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))

    # write the headers
    writer.writerow([
        smart_str(u"Platform"),
        smart_str(u"Data"),
        smart_str(u"Time Spent"),
        smart_str(u"Timestamp"),
    ])

    # get data from database
    linked_platforms = person.linked_platforms
    for platform_index in range(len(linked_platforms)):
        platform = linked_platforms[platform_index]
        platform.name = platform.platform
        data_arr = platform.data
        for data_obj in data_arr:
            writer.writerow([
                smart_str(platform.name),
                smart_str(data_obj.raw_data),
                smart_str(data_obj.spent_minutes),
                smart_str(data_obj.timestamp_epoch),
            ])

    return response
