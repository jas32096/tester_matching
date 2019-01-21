from user_search import *
import sys
import json
from collections import OrderedDict

def _parse(args):
    '''
    Manual parsing. Pass args as CSV

    usage: user_search 'US, JP' 'iPhone 4' [True/False]
    '''
    try:
        if len(args) > 3: raise IndexError
        countries = [i.strip() for i in args[0].split(',')]
        devices = [i.strip() for i in args[1].split(',')]
        if len(args) >= 3:
            should_show_devices = args[2].lower() == 'true'
        else:
            should_show_devices = False
    except IndexError as e:
        print('Bad Input', file=sys.stderr)
        sys.exit(1)

    if 'ALL' in countries: countries = None
    if 'ALL' in devices: devices = None

    return {
        'countries': countries,
        'devices': devices,
        'should_show_devices': should_show_devices
    }

def search(countries: list, devices: list, should_show_devices=False, fmt='normal', file=sys.stdout):
    if fmt not in {'normal', 'tsv', 'json'}: return 1

    # Case conversions for basic case-insensitivity
    for i in range(len(countries or [])): countries[i] = countries[i].upper()
    for i in range(len(devices or [])): devices[i] = devices[i].lower()

    qry = session.query(Tester).join(TesterExperience).order_by(TesterExperience.experience.desc())
    if countries:
        qry = qry.filter(Tester.country.in_(countries))
    if devices:
        qry = qry.filter(Tester.device_collection.any(Device.description_lower.in_(devices)))

    if fmt == 'json':
        out = OrderedDict({
            'testers': [{'Name': tester.fullName,
                         'ID': tester.testerId,
                         'Country': tester.country,
                         'Experience': tester.experience,
                         'Last Login': tester.lastLogin,
                         'devices': [i.description for i in tester.device_collection]}
                       for tester in qry],
            'total': qry.count()
        })
        print(json.dumps(out), file=file)
    else:
        not_tsv = fmt != 'tsv'
        print('Name\tID\tCountry\tExperience\tLast Login', file=file)
        longest_name = 4
        for tester in qry:
            if len(tester.fullName) > longest_name:
                longest_name = len(tester.fullName)
            print(f"{tester.fullName}\t{tester.testerId}\t{tester.country}\t{tester.experience}\t{tester.lastLogin}", file=file)
            if should_show_devices and not_tsv:
                print(f"   {[i.description for i in tester.device_collection]}", file=file)
        if not_tsv:
            print('-'*(longest_name+1), file=file)
            print(f"Total {qry.count()}", file=file)

    return 0