#!/usr/bin/env python3

import argparse
import json
import os
import requests

def get_title(requirement_file):
    return f"Auto-update outdated dependencies in {requirement_file}"


def find_replace_in_file(file_path, find_str, replace_str):
    with open(file_path, 'r') as file:
        content = file.read()
    content = content.replace(find_str, replace_str)
    with open(file_path, 'w') as file:
        file.write(content)


def create_branch_if_not_exists(headers, repo, branch, commit_sha):
    response = requests.get(f"https://api.github.com/repos/{repo}/branches/{branch}")
    if response.status_code == 404: 
        refs = {"ref":"refs/heads/" + branch, "sha": commit_sha}
        headers["Accept"] = f"application/vnd.github+json"
        response = requests.post(f"https://api.github.com/repos/{repo}/git/refs", headers=headers, data=json.dumps(refs))
        if response.status_code == 201: 
            print(f"INFO: Branch created -> https://github.com/{repo}/tree/{branch}")
        else:
            print("ERROR: branch not created")
    else:
        print("INFO: the branch already esists")


def create_commit_on_branch_with_changes(branch, file_to_change):
    commit_message = f"Update {file_to_change}"
    os.system(f"git add {file_to_change}")
    os.system(f"git commit --message=\"{commit_message}\"")
    os.system(f"git push origin {branch}")


if __name__ == '__main__':
    # Arguments parsing
    parser = argparse.ArgumentParser(description="Manage pr with the correct argument")
    parser.add_argument("requirement_file", type=str, help='The path to the requirement file')
    parser.add_argument("package", type=str, help='The name of the package')
    parser.add_argument("version", type=str, help='The current version of the package')
    parser.add_argument("latest", type=str, help='The latest version of the package')
    args = parser.parse_args()
    # TODO: check if arguments are filled, if not exit with errors

    # Environment variable
    token = str(os.environ.get("GITHUB_TOKEN"))
    repo = str(os.environ.get("GITHUB_REPOSITORY"))
    commit_sha = str(os.environ.get("GITHUB_SHA"))
    requirement_file = str(os.environ.get("REQUIREMENT_FILE"))

    # Set utility variables
    headers = {"Authorization": f"token {token}"}
    branch = "check_outdated_dependencies"
    create_branch_if_not_exists(headers, repo, branch, commit_sha)

    # Replace the line
    line_current = f"{args.package}=={args.version}"
    line_new = f"{args.package}=={args.latest}"
    find_replace_in_file(args.requirement_file, line_current, line_new)

    # TODO: spot the problem here: https://github.com/Wabri/community.sap_install/actions/runs/8378748459/job/22944046135
    create_commit_on_branch_with_changes(branch, requirement_file)

