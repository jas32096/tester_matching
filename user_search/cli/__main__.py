import sys

from user_search.cli.cli import search, _parse

if __name__ == '__main__':
    args = sys.argv[1:]

    try:
        import argparse
        parser = argparse.ArgumentParser(prog='user_search')
        parser.add_argument('-c', '--countries', nargs='+', help='No value includes all')
        parser.add_argument('-d', '--devices', nargs='+', help='No value includes all')
        parser.add_argument('--show-devices', dest='should_show_devices', action='store_true', default=False, help='Always True with --json and False with --tsv')
        fmt = parser.add_mutually_exclusive_group()
        fmt.add_argument('-f', '--format', dest='fmt', choices=('normal', 'tsv', 'json'), default='normal')
        fmt.add_argument('--json', dest='fmt', action='store_const', const='json')
        fmt.add_argument('--tsv', dest='fmt', action='store_const', const='tsv')
        sub = parser.add_subparsers()
        old = sub.add_parser('force-old-style')
        old.add_argument(dest='old_args', nargs='+')
        
        parsed = parser.parse_args(args)
        if hasattr(parsed, 'old_args'):
            args = parsed.old_args
            e = ModuleNotFoundError()
            e.ok = True
            raise e

        kwargs = vars(parsed)
    except ModuleNotFoundError as e:
        # If argprase doesn't exist for some reason
        # we can fallback to just using argv
        if not hasattr(e, 'ok'):
            print('Warning: argparse not found. Forcing old style', file=sys.stderr)
            print(_parse.__doc__, file=sys.stderr)

        kwargs = _parse(args)

    sys.exit(search(**kwargs))