# Copyright (C) 2021  Patrick Totzke <patricktotzke@gmail.com>
# This file is released under the GNU GPL, version 3 or a later revision.

import sys
import json
import logging
import argparse
import os
import yaml
from jinja2 import Template

import grade50

DEFAULT_TMPLATE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'templates',
    'default.jinja2')


def main():
    helpmsg = """
    turn the output of `check50 -o json` into plaintext feedback
    """
    parser = argparse.ArgumentParser(description=helpmsg)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('scheme', type=argparse.FileType('r'))
    parser.add_argument('report', type=argparse.FileType('r'), default='-')
    parser.add_argument("-o", "--output",
                        action="store",
                        default="ansi",
                        choices=["ansi", "json"],
                        help="output format")
    parser.add_argument('-t', '--template',
                        type=argparse.FileType('r'),
                        default=None,
                        help='jinja2 template for ansi output')
    parser.add_argument('-V', '--version', action='version',
                        version=grade50.__version__,
                        help='output version information and exit')

    _LOG_LEVEL_STRINGS = [logging.ERROR, logging.INFO, logging.DEBUG]

    def read_report(f):
        """turn list of results into a map name->result"""
        data = json.load(f)
        res = {}
        for r in data['results']:
            res[r['name']] = r
        return res

    def read_scheme(f):
        return yaml.load(f, Loader=yaml.FullLoader)

    args = parser.parse_args()
    logging.basicConfig(
            level=_LOG_LEVEL_STRINGS[args.verbose],
            format='%(message)s',
            )

    logging.debug("load marking scheme")
    scheme = read_scheme(args.scheme)

    logging.debug("load json input")
    report = read_report(args.report)

    entry = {'parts': [], 'points': 0, 'points_possible': 0}
    for spart in scheme:
        cmt = []
        points = 0
        points_possible = 0
        for scheck in spart['checks']:
            name = scheck['name']
            rcheck = report[name]
            points_possible += scheck['points']
            logging.debug(rcheck)
            if rcheck['passed'] == True:
                points += scheck['points']
                if 'pass_comment' in scheck:
                    logging.debug(scheck['pass_comment'].format(**rcheck))
                    cmt.append(scheck['pass_comment'].format(**rcheck))
            elif rcheck['passed'] == False:
                if 'fail_comment' in scheck:
                    logging.debug(scheck['fail_comment'].format(**rcheck))
                    cmt.append(scheck['fail_comment'].format(**rcheck))
            else:
                # null, indicates that the check did not run due to a
                # dependency failing
                pass

        entry['points'] += points
        entry['points_possible'] += points_possible
        entry['parts'] += [{
            'name': spart['name'],
            'points': points,
            'points_possible': points_possible,
            'comments': cmt
        }]

    logging.info("output")
    if args.output == 'json':
        output = json.dumps(entry, indent=2)

    elif args.output == 'ansi':
        # open default template if none is given
        if args.template is None:
            args.template = open(DEFAULT_TMPLATE_PATH)

        # run rendering engine
        try:
            template = Template(args.template.read())
            output = template.render(**entry)
        except Exception as e:
            msg = "Cannot render report: "
            logging.exception(e)
            msg += e.args[0]
            sys.exit(1)
    print(output)


if __name__ == "__main__":
    main()
