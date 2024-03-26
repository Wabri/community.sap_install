#!/usr/bin/env python3

import argparse
import os
import re


def build_packages_dict_from_file(requirement_file):
    with open(requirement_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            regex_pattern = re.compile(
                "([a-zA-Z0-9-]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([a-zA-Z]+)")
            search_result = regex_pattern.search(line)
            search_result.group(1)
            search_result.group(2)
            search_result.group(3)


def build_packages_dict_from_output(output):
    print("TODO")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Dependabot clone arguments")
    parser.add_argument(
        "requirement_file", type=str,
        help='The path to the requirement file')
    args = parser.parse_args()

    os.system(f"pip3 install -r {args.requirement_file}")
    raw_output_outdated = os.system("pip3 list --outdated")
    current_packages = build_packages_dict_from_file(args.requirement_file)
    latest_packages = build_packages_dict_from_output(raw_output_outdated)

    print("######")
    print(raw_output_outdated)
    print("######")
