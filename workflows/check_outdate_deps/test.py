#!/usr/bin/env python3

import os
import re


def build_packages_dict_from_file(requirement_file):
    with open(requirement_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            regex_pattern = re.compile(
                "([a-zA-Z0-9-]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([a-zA-Z]+)")
            regex_pattern.findall(line)


def build_packages_dict_from_output(output):
    print("TODO")


if __name__ == '__main__':
    requirement_file = str(os.environ.get("REQUIREMENT_FILE"))

    os.system(f"pip3 install -r {requirement_file}")
    raw_output_outdated = os.system("pip3 list --outdated")
    current_packages = build_packages_dict_from_file(requirement_file)
    latest_packages = build_packages_dict_from_output(raw_output_outdated)

    print("######")
    print(raw_output_outdated)
    print("######")
