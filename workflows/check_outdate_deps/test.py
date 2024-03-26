#!/usr/bin/env python3

import argparse
import os

def build_packages_dict_from_file(requirement_file):
    print("TODO")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Manage pr with the correct argument")
    parser.add_argument("requirement_file", type=str, help='The path to the requirement file')
    args = parser.parse_args()
    current_packages = build_packages_dict_from_file(args.requirement_file)

    os.system(f"pip3 install -r {args.requirement_file}")
    raw_output_outdated = os.system("pip3 list --outdated")

    print(raw_output_outdated)
