#!/usr/bin/env bash

# Tells the shell to exit immediately if any command exits with a non-zero 
# status
set -o errexit 
# Treat unset variables as an error when they are referenced
set -o nounset
# Return the exit status of the last command in a pipeline that returned a 
# non-zero status
set -o pipefail

# Print each command line before executing it, useful for debugging
if [[ "${TRACE-0}" == "1" ]]; then
  set -o xtrace
fi

compare_versions() {
   local version1=$1 
   local version2=$2
   local IFS='.'

   read -ra version1_splitted <<< "$version1"
   read -ra version2_splitted <<< "$version2"

   for ((i=0;i<${#version1_splitted[@]};i++)); do
       delta=$(( version1_splitted[i] - version2_splitted[i] ))
       if (( delta != 0 )); then
           echo $delta
           return
       fi
   done
   echo 0
}

is_pakage_included_in_requirement_file() {
    for i in "${packages[@]}"; do
        if [ "$i" == "$1" ]; then
            return 0
        fi
    done
    return 1
}

main() {
    # Parse requirement file to extract all packages
    packages=()
    requirement_content=`cat $REQUIREMENT_FILE`
    while read -r line; do
        if [[ $line =~ ^([a-zA-Z\-]+)=+(([0-9]+\.)*[0-9]+) ]]; then
            packages+=("${BASH_REMATCH[1]}")
        fi
    done <<< "$requirement_content"
    
    # Install all packages from requirement file and check if there are any
    # outdated packages
    pip3 install -r "$REQUIREMENT_FILE"
    input=$(pip3 list --outdated)
    
    while read -r line; do
        if [[ $line =~ ^([a-zA-Z0-9-]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([0-9]+\.[0-9]+\.[0-9]+)\ +([a-zA-Z]+) ]]; then
            package="${BASH_REMATCH[1]}"
            version="${BASH_REMATCH[2]}"
            latest="${BASH_REMATCH[3]}"
            
            if [ "$(compare_versions "$version" "$latest")" -lt 0 ] && \
               is_pakage_included_in_requirement_file "$package"; then
                    ./workflows/check_outdate_deps/open_issue.py \
                        "$package" \
                        "$version" \
                        "$latest"
            fi
        fi
    done <<< "$input"
    if [ "$OPEN_PR" == "True" ]; then
        ./workflows/check_outdate_deps/manage_pr.py \
            "$REQUIREMENT_FILE" \
            "$package" \
            "$version" \
            "$latest"
    fi
}

main "$@"
