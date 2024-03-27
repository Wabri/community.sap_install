#!/usr/bin/env python3

import os
import re
import subprocess


def build_packages_dict_from_file(requirement_file):
    print("-------------")
    print("INFO: create dict from file")
    packages = {}
    with open(requirement_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            regex_pattern = re.compile(
                "([a-zA-Z0-9-]+)==([0-9]+\.[0-9]+\.[0-9]+)")
            matches = regex_pattern.findall(line)
            packages |= {str(matches[0][0]): str(matches[0][1])}
    return packages


def build_packages_dict_from_output(output):
    print("-------------")
    print("INFO: create dict from output")
    packages = {}
    lines = output.splitlines(output)
    for line in lines:
        regex_pattern = re.compile(
            "([a-zA-Z0-9-]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([a-zA-Z]+)")
        matches = regex_pattern.findall(line)
        packages |= {str(matches[0][0]): str(matches[0][2])}
    return packages


if __name__ == '__main__':
    requirement_file = str(os.environ.get("REQUIREMENT_FILE"))

    os.system(f"pip3 install -r {requirement_file}")
    raw_output_outdated = subprocess.run(
        ['pip3', 'list', '--outdated'],
        stdout=subprocess.PIPE)
    current_packages = build_packages_dict_from_file(requirement_file)
    latest_packages = build_packages_dict_from_output(
        raw_output_outdated.stdout.decode('utf-8'))

    print("-------------")
    print("INFO: Check outdated dependencies")
    for package in current_packages.keys():
        if package in latest_packages:
            print(f"""
            package: {package} current: {current_packages[package]} latest: {latest_packages[package]}
            """)
