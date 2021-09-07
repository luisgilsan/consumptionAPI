from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

# Class MUST be named 'Command'
class Command(BaseCommand):

    # Displayed from 'manage.py help mycommand'
    help = "That's Your help message"

    # make_option requires options in optparse format
    # option_list = BaseCommand.option_list  + (
    #                     make_option('--myoption', action='store',
    #                         dest='myoption',
    #                         default='default',
    #                         help='Option help message'),
    #               )

    def handle(self, *app_labels, **options):
        """
        app_labels - app labels (eg. myapp in "manage.py reset myapp")
        options - configurable command line options
        """
        print('...')
        print('Tarea creada')
        print('...')