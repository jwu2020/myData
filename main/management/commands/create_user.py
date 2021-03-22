from django.core.management.base import BaseCommand, CommandError
from main.bin.forms.add_user import add_user

'''
Creates new main in mongoDBDatabase and populates fields.

CLI: python3 manage.py create_user <insert username> <insert password>

'''


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('user_details', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        email = kwargs['user_details'][0]
        password = kwargs['user_details'][1]
        person = add_user(email, password)
        self.stdout.write(self.style.SUCCESS('Successfully created main %s' % person))



