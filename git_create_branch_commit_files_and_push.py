import argparse
import subprocess
import sys

import os
import git


def create_branch(arguments):
    # Create a new branch with the given name, or use the current branch if none is specified
    if arguments.branch_name:
        try:
            output = subprocess.run(["git", "checkout", "-b", arguments.branch_name], check=False)
            if output.returncode:
                subprocess.run(["git", "checkout", arguments.branch_name], check=False)
        except subprocess.CalledProcessError:
            print(f"Error: invalid branch name '{arguments.branch_name}'")
            sys.exit(1)
    else:
        # Get the current branch name
        try:
            result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, check=True)
            arguments.branch_name = result.stdout.decode().strip()
        except subprocess.CalledProcessError:
            print("Error: not a Git repository")
            sys.exit(1)

def add_and_commit_message(commit_message):
    # Commit the changes with the given commit message
    if commit_message:
        subprocess.run(["git", "commit", "-am", commit_message])
    else:
        print("Error: could not commit files. commit message expected")
        sys.exit(1)

def commit(arguments):
    # Add the specified files to the staging area, or add all modified files if none are specified
    if arguments.files:
        try:
            subprocess.run(["git", "add"] + arguments.files, check=True)
            # Commit the changes with the given commit message
            try:
                subprocess.run(["git", "commit", "-m", arguments.commit_message])
            except subprocess.CalledProcessError:
                print(f"Error: could not commit files: '{arguments.files}'")
                sys.exit(1)
        except subprocess.CalledProcessError:
            print(f"Error: one or more files could not be added")
            sys.exit(1)
    else:
        add_and_commit_message(arguments.commit_message)


def commit_toplevel():
    """Extracts the changed lines from a git diff output.
        Submodule libraries/thirdparty_googletest contains modified content
        Submodule libraries/thirdparty_googletest 52310c4e5..bd09af8d8:
          > some changes due to the new google test tag
        Submodule libraries/thirdparty_gunit 9bb6a5771..0e16335dd:
          > some changes due to the new google test tag
        Submodule libraries/time_backupper contains modified content
        Submodule plustools/pluscontrol_srv contains modified content

    Args:
      diff_output: The output of the `git diff` command.

    Returns:
      A list of tuples, where each tuple contains the following:
        * The name of the file that changed.
        * A list of line numbers that changed.
    """
    # Get the git diff output.
    diff_output = subprocess.check_output(['git', 'diff'])

    # Extract the changed lines from the git diff output.
    chars_to_look_for = [':', '>']
    changed_lines = ''
    for line_bytes in diff_output.splitlines():
        line = str(line_bytes)
        for char_to_look_for in chars_to_look_for:
            if char_to_look_for in line:
                changed_lines += (line[2:-1] + '\n')

    add_and_commit_message(changed_lines)


def push(arguments):
    try:
        # Push the new branch to the remote repository
        if arguments.force:
            subprocess.run(["git", "push", "--force", "origin", arguments.branch_name])
        else:
            subprocess.run(["git", "push", "origin", arguments.branch_name])
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)


def is_toplevel_git_directory_with_submodules():
    try:
        return os.path.exists(".git/modules")

    except subprocess.CalledProcessError:
        return False


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--branch_name",
                        help="the name of the new branch (optional, defaults to the current branch)", default=None)
    parser.add_argument("-f", "--force", help="force push", action='store_true')
    parser.add_argument("commit_message", help="the commit message", nargs="?")
    parser.add_argument("files", help="a list of files to commit (optional, defaults to all modified files)", nargs="*")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()

    create_branch(arguments)

    if is_toplevel_git_directory_with_submodules():
        commit_toplevel()
    else:
        commit(arguments)

    push(arguments)
