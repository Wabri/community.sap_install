#!/usr/bin/env python3

import os
import re
import subprocess


def build_packages_dict_from_file(requirement_file):
    print("-------------")
    print("from file")
    with open(requirement_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            regex_pattern = re.compile(
                "([a-zA-Z0-9-]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([a-zA-Z]+)")
            regex_pattern.findall(line)


def build_packages_dict_from_output(output):
    print("-------------")
    print("from output")
    print(output)


if __name__ == '__main__':
    requirement_file = str(os.environ.get("REQUIREMENT_FILE"))

    os.system(f"pip3 install -r {requirement_file}")
    raw_output_outdated = subprocess.run(
        ['pip3', 'list', '--outdated'],
        stdout=subprocess.PIPE)
    current_packages = build_packages_dict_from_file(requirement_file)
    latest_packages = build_packages_dict_from_output(
        raw_output_outdated.stdout)
