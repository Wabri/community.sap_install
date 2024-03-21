#!/usr/bin/env python3

import argparse

def get_title(requirement_file):
    return f"Auto-update outdated dependencies in {requirement_file}"

def find_replace_in_file(file_path, find_str, replace_str):
    with open(file_path, 'r') as file:
        content = file.read()
    content = content.replace(find_str, replace_str)
    with open(file_path, 'w') as file:
        file.write(content)

if __name__ == '__main__':
    # Arguments parsing
    parser = argparse.ArgumentParser(description="Manage pr with the correct argument")
    parser.add_argument("requirement_file", type=str, help='The path to the requirement file')
    parser.add_argument("package", type=str, help='The name of the package')
    parser.add_argument("version", type=str, help='The current version of the package')
    parser.add_argument("latest", type=str, help='The latest version of the package')
    args = parser.parse_args()

    # Compose line in file to replace
    line_current = f"{args.package}=={args.version}"
    line_new = f"{args.package}=={args.latest}"
    find_replace_in_file(args.requirement_file, line_current, line_new)

