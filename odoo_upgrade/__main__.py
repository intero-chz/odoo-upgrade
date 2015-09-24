#!/usr/bin/env python
#-*- encoding: utf8 -*-

from __future__ import absolute_import

import argparse

from .version import __version__
from .odoo_upgrade import UpgradeManager

DEFAULT_URL = "https://upgrade.odoo.com"
TARGETS = "6.0 6.1 7.0 8.0".split()


parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    'action', choices=['create', 'upload', 'process', 'status'],
    help="Action to perform. Choices: %(choices)s", action='store',
    metavar='ACTION',
    nargs='?')
verb = parser.add_mutually_exclusive_group()
verb.add_argument(
    '-q', '--quiet', help="Quiet output", dest="verbose", default=[1],
    action='store_const', const=[])
verb.add_argument(
    '-v', '--verbose', dest="verbose", default=[],
    action='append_const', const=1,
    help=("Verbose output.\n"
          "Use -q, --quiet to make it quiet"))
verb.add_argument(
    '-V', '--version',
    action='version', version='%(prog)s (version {})'.format(__version__),
    help="Display version information")

request_group = parser.add_argument_group("Request arguments")
request_group.add_argument(
    '--contract', action='store', metavar='CONTRACT',
    help="Your Enterprise contarct reference")
request_group.add_argument(
    '--email', action='store', metavar='ADDRESS',
    help="Your email address")
request_group.add_argument(
    '--target', choices=TARGETS, action='store',
    metavar='VERSION',
    help="Odoo target version\nChoices: %(choices)s")
request_group.add_argument(
    '--filename', action='store',
    help="Name of your dump file. Purely informative")
request_group.add_argument(
    '--aim', choices=['test', 'production'],
    action='store', metavar='AIM',
    help=("Purpose of your request. Upgrade for test or\n"
          "upgrade for production use.\nChoices: %(choices)s"))
request_group.add_argument(
    '--timezone', default=False,
    action='store', metavar='TZ',
    help="Server timezone (for Odoo <6.1)")
request_group.add_argument(
    '--key', action='store', metavar='PRIVATE_KEY',
    help=("Your request private key.\n"
          "Use the 'status' action if you want to retrieve this information.\n"
          "Query the 'key' parameter"))
request_group.add_argument(
    '--request', action='store', metavar='ID',
    help=("Your request id.\n"
          "Use the 'status' action if you want to retrieve this information.\n"
          "Query the 'id' parameter"))
request_group.add_argument(
    '--dbdump', action='store', metavar='PATH',
    help=("The path to your database dump file"))

obscure_group = parser.add_argument_group(
    "Obscure arguments that you should not use")
obscure_group.add_argument(
    '--insecure', default=False,
    action='store_true',
    help=("This option explicitly allows performing \"insecure\" SSL\n"
          "connections and transfers. By default, all SSL connections\n"
          "are attempted to be made secure by using the CA certificate\n"
          "bundle installed"))
obscure_group.add_argument(
    '--url', default=DEFAULT_URL,
    help="Upgrade platform URL (default: %(default)s)", action='store',
    metavar='URL')
obscure_group.add_argument(
    '--debug', default=False,
    help="Debug", action='store_true',)


def main():
    args = parser.parse_args()
    app = UpgradeManager(args)
    app.run()

if __name__ == '__main__':
    main()
