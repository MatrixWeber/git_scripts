#!/bin/bash

 

# Fetch the latest remote branches

git fetch --all

 

# Get the list of last 10 remote branches committed

branches=$(git for-each-ref --sort=-committerdate --format='%(refname:short)|%(committerdate:iso)|%(committername)' refs/remotes/origin | head -n 10)

 

# ANSI escape codes for color formatting

color_branch="\033[1;35m"        # Magenta (branch name)

color_commit_datetime="\033[1;34m"   # Blue (commit date)

color_committer="\033[1;32m"     # Green (committer name)

color_reset="\033[0m"            # Reset color

 

# Display the list of branches with committer info and numbers

echo -e "Recent remote branches:"

i=1

IFS=$'\n'

for branch_info in $branches; do

    IFS='|' read -ra branch_data <<< "$branch_info"

    branch_name="${branch_data[0]}"

    commit_datetime="${branch_data[1]}"

    committer_name="${branch_data[2]}"

 

    # Remove "origin/" prefix from the branch name

    branch_name=$(echo "$branch_name" | sed 's/^origin\///')

 

    printf "%-4s ${color_commit_datetime}%-10s${color_reset} ${color_committer}%-20s${color_reset} ${color_branch}%-30s${color_reset}\n" "$i." "$commit_datetime" "$committer_name" "$branch_name"

    ((i++))

done

 

# Ask the user to select a branch

echo -n "Enter the number of the branch to checkout: "

read choice

 

# Checkout the selected branch

selected_branch=$(echo "$branches" | sed -n "${choice}p" | awk -F '|' '{print $1}' | sed 's/^origin\///')

if [ -n "$selected_branch" ]; then

    git checkout "$selected_branch"

    git pull origin "$selected_branch"

    git submodule update --init

else

    echo "Invalid choice."

fi