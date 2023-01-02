import argparse
import subprocess
import sys


def create_branch(branch_name, commit_message, files):
    # Create a new branch with the given name, or use the current branch if none is specified
    if branch_name:
        try:
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        except subprocess.CalledProcessError:
            print(f"Error: invalid branch name '{branch_name}'")
            sys.exit(1)
    else:
        # Get the current branch name
        try:
            result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, check=True)
            branch_name = result.stdout.decode().strip()
        except subprocess.CalledProcessError:
            print("Error: not a Git repository")
            sys.exit(1)

    # Add the specified files to the staging area, or add all modified files if none are specified
    if files:
        try:
            subprocess.run(["git", "add"] + files, check=True)
            #Commit the changes with the given commit message
            try:
                subprocess.run(["git", "commit", "-am", commit_message])
            except subprocess.CalledProcessError:
                print("Error: could not commit files")
                sys.exit(1)
        except subprocess.CalledProcessError:
            print(f"Error: one or more files could not be added")
            sys.exit(1)
    else:
        # Commit the changes with the given commit message
        try:
            subprocess.run(["git", "commit", "-am", commit_message])
        except subprocess.CalledProcessError:
            print("Error: could not commit files")
            sys.exit(1)

    try:
        # Push the new branch to the remote repository
        subprocess.run(["git", "push", "origin", branch_name])
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)


# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--branch_name", help="the name of the new branch (optional, defaults to the current branch)", default=None)
parser.add_argument("commit_message", help="the commit message")
parser.add_argument("files", help="a list of files to commit (optional, defaults to all modified files)", nargs="*")
args = parser.parse_args()

# Create the new branch
create_branch(args.branch_name, args.commit_message, args.files)
