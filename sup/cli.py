"""
Functions that perform actions via the command line interface.
"""
from datetime import datetime, timedelta
import os

from dateutil.parser import parse as dateparse

from . import config
from . import sup


def execute_args(args):
    """
    Parses options and writes/opens the file.
    """
    if not os.path.exists(config.ARCHIVE_DIR):
        os.mkdir(config.ARCHIVE_DIR)

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    if args.get('--update'):

        if args.get('--date'):
            previous_date = dateparse(args['--date'])
        elif args.get('--last'):
            previous_date = sup.find_last_date(verbose=args['--verbose'])
        else:
            previous_date = today - timedelta(days=1)

        sup.create_update(previous_date, today, verbose=args['--verbose'])
        sup.open_file(today, verbose=args['--verbose'])

    elif args.get('--print'):

        if args.get('--date'):
            print_date = dateparse(args['--date'])
        else:
            print_date = today

        sup.print_sup(print_date, verbose=args['--verbose'])

    elif args.get('--config'):
        does_exist = os.path.exists(config.CONFIG_PATH)
        print(
            'Config %s at path "%s"' % (
                'exists' if does_exist else 'does not exist',
                config.CONFIG_PATH
            )
        )
        print('contents: %s' % config.CONFIG)

    elif args.get('--date'):
        archive_date = dateparse(args['--date'])
        sup.create_file(archive_date, verbose=args['--verbose'])
        sup.open_file(archive_date, verbose=args['--verbose'])

    elif args.get('--last'):
        sup.open_file(sup.find_last_date(), verbose=args['--verbose'])

    elif args.get('--yesterday'):
        sup.open_file(yesterday, verbose=args['--verbose'])

    elif args.get('--tomorrow'):
        sup.create_file(tomorrow, verbose=args['--verbose'])
        sup.open_file(tomorrow, verbose=args['--verbose'])

    elif args.get('--new'):
        new_file = sup.create_file(today, new=True, verbose=args['--verbose'])
        sup.open_file(filepath=new_file, verbose=args['--verbose'])

    elif args.get('--iteration'):
        i_file = sup.create_file(today, i=args['--iteration'], verbose=args['--verbose'])
        sup.open_file(filepath=i_file, verbose=args['--verbose'])

    elif args.get('--review'):
        review_file = sup.create_review_file(today, verbose=args['--verbose'])
        sup.open_file(filepath=review_file, verbose=args['--verbose'])

    elif args.get('--dir'):
        print(config.ARCHIVE_DIR)

    elif args.get('--version'):
        import pkg_resources
        print('Sup version: %s' % pkg_resources.get_distribution('sup'))

    else:
        sup.create_file(today, verbose=args['--verbose'])
        sup.open_file(today, verbose=args['--verbose'])
