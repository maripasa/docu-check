#!/usr/bin/env python3

import argparse
import logging
import sys

from lib.log.logger import setup_logging

from old_docucheck.core import DocuCheck

VERSION = "v0.0.2"

HELP_MSGS = {

    "debug": "Debug mode.",
    "single_check": "Scrapes and checks the documents of a company once.",
    "email": "Email to send the report.",
    "cnpj": "CNPJ of the company to check.",
    "no_headless": "Run the browser in headless mode.",
    "version": "Show the current docucheck version.",
}


def parse(args):
    if args.no_headless:
        print("Does nothing yet")
    if args.single_check:
        print("Does nothing yet")

    if args.cnpj is not None and args.email is not None:
        cnpj = args.cnpj
        email = args.email
    else:
        print("You need an email and a CNPJ to run the program.")
        sys.exit(1)

    verifier = DocuCheck(receiver_cnpj=cnpj, receiver_email=email)
    verifier.execute()


def main():
    def help_formatter(prog):
        return argparse.RawTextHelpFormatter(prog, max_help_position=26)

    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPÇÕES]",
        formatter_class=help_formatter,
    )
    parser.add_argument('--debug', '-d', action="store_true", help=HELP_MSGS["debug"])
    parser.add_argument('--single_check', '-s', help=HELP_MSGS["single_check"])
    parser.add_argument('--email', '-e', default=None, help=HELP_MSGS["email"])
    parser.add_argument('--cnpj', '-c', default=None, help=HELP_MSGS["cnpj"])
    parser.add_argument("--no_headless", action="store_true", help=HELP_MSGS["no_headless"])
    parser.add_argument("--version", action="store_true", help=HELP_MSGS["version"])

    args = parser.parse_args()

    if args.version:
        print("docucheck " + VERSION)
        sys.exit(0)

    if args.debug:
        setup_logging()
    else:
        logging.basicConfig()

    try:
        parse(args)
    except KeyboardInterrupt:
        sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    main()
