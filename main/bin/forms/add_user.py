from main.models import User, Notification, LinkedPlatform, Data, SummaryStats, FacebookEntry, YTEntry, NetflixEntry, GoogleEntry
from django.utils import timezone


def add_user(email, password):
    """
    Adds user to database and populates their email and pw
    :param email: email string
    :param password: plain text pw
    :return: person object
    """
    
    # Instantiate main and populate fields
    person = User()
    person.notifications = [Notification()]

    person.linked_platforms = []
    platform_arr = ['fb', 'yt', 'netflix', 'google']

    # Create placeholder for platforms
    for platform in platform_arr:
        platform_obj = LinkedPlatform()
        platform_obj.platform = platform
        person.linked_platforms.append(platform_obj)

    for lp in person.linked_platforms:
        data_obj = Data()
        lp.data = [data_obj]

    # Create placeholder for summary stats
    person.summary_stats = [SummaryStats()]

    for sp in person.summary_stats:
        sp.timestamp = timezone.now()
        sp.fb = FacebookEntry()
        sp.yt = YTEntry()
        sp.netflix = NetflixEntry()
        sp.google = GoogleEntry()

    person.username = email
    person.password = password
    person.save()


    return person