#!/usr/bin/env python3

import os
import re
import subprocess
import requests
import json


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
            if len(matches) > 0:
                package_name = str(matches[0][0])
                package_version = str(matches[0][1])
                packages[package_name] = package_version
    return packages


def open_issue_for_package(package, current_version, latest_version):
    repo = os.environ.get("GITHUB_REPOSITORY")
    requirement_file = str(os.environ.get("REQUIREMENT_FILE"))
    issue_title = f"""
Dependency outdated in {requirement_file}:
{package}=={current_version} -> {latest_version}
    """
    query = f"repo:{repo} type:issue in:title \"{issue_title}\""
    response = requests.get(
        "https://api.github.com/search/issues", params={"q": query})
    data = response.json()
    if data["total_count"] > 0:
        print("There is already an issue with this title!")
        print(data)
    else:
        issue_description = f"""
        The package {package} is outdated in {requirement_file}.

        The latest version is {latest_version}. Please update the package to the latest version.

        Check the package [here](https://pypi.org/project/{package}/{latest_version}/) for more information.
        """
        token = os.environ.get("GITHUB_TOKEN")
        issue = {"title": issue_title, "body": issue_description}
        headers = {"Authorization": f"token {token}"}
        response = requests.post(
            f"https://api.github.com/repos/{repo}/issues",
            headers=headers,
            data=json.dumps(issue))

        # Check the response
        if response.status_code == 201:
            print("Issue created successfully.")
            data = response.json()
            print(data['number'])
        else:
            print(f"Failed to create issue. Status code: {
                  response.status_code}.")


def build_packages_dict_from_output(output):
    print("-------------")
    print("INFO: create dict from output")
    packages = {}
    lines = output.splitlines(output)
    for line in lines:
        regex_pattern = re.compile(
            "([a-zA-Z0-9-]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([a-zA-Z]+)")
        matches = regex_pattern.findall(line)
        if len(matches) > 0:
            package_name = str(matches[0][0])
            package_version = str(matches[0][2])
            packages[package_name] = package_version
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
            current_version = current_packages[package]
            latest_version = latest_packages[package]
            print(f"""
            package: {package}
            current: {current_version}
            latest: {latest_version}
            """)

            # TODO: Open Issue
            open_issue_for_package(package, current_version, latest_version)

            # TODO: if OPEN_PR env var is set to true than apply the changes
            #   and open the pr
