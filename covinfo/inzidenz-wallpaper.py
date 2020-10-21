#!/usr/bin/env python3

import argparse



parser = argparse.ArgumentParser(description='Make a screensaver with the latest covid numbers')
parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbosity turned on")
