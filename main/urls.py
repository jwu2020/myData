from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main.html'),
    path('accounts', views.accounts, name='accounts.html'),
    path('detailed_yt', views.detailed_yt, name='detailed.html'),
    path('detailed_google', views.detailed_google, name='detailed.html'),
    path('detailed_fb', views.detailed_fb, name='detailed.html'),
    path('detailed_netflix', views.detailed_netflix, name='detailed.html'),
    path('goals', views.goals, name='goals.html'),
    path('login', views.Login.as_view(), name='login.html'),
    path('logout', views.logMeOut, name='login.html'),
    path('main', views.main, name='main.html'),
    path('register', views.main, name='register.html'),
    path('download', views.download, name='download'),
    path('ajax/disconnect', views.disconnect, name='disconnect'),
    path('ajax/connect', views.connect, name='connect'),
    path('ajax/update_goal', views.update_goal, name='update_goal'),
    path('ajax/check_notifications', views.check_notifications, name='check_notifications'),
    path('poll', views.poll, name='poll')

]

