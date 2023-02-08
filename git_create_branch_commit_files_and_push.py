import argparse
import subprocess
import sys


def create_branch(args):
    # Create a new branch with the given name, or use the current branch if none is specified
    if args.branch_name:
        try:
            subprocess.run(["git", "checkout", "-b", args.branch_name], check=False)
        except subprocess.CalledProcessError:
            print(f"Error: invalid branch name '{args.branch_name}'")
            sys.exit(1)
    else:
        # Get the current branch name
        try:
            result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, check=True)
            args.branch_name = result.stdout.decode().strip()
        except subprocess.CalledProcessError:
            print("Error: not a Git repository")
            sys.exit(1)

    # Add the specified files to the staging area, or add all modified files if none are specified
    if args.files:
        try:
            subprocess.run(["git", "add"] + args.files, check=True)
            #Commit the changes with the given commit message
            try:
                subprocess.run(["git", "commit", "-m", args.commit_message])
            except subprocess.CalledProcessError:
                print(f"Error: could not commit files: '{args.files}'")
                sys.exit(1)
        except subprocess.CalledProcessError:
            print(f"Error: one or more files could not be added")
            sys.exit(1)
    else:
        # Commit the changes with the given commit message
        try:
            subprocess.run(["git", "commit", "-am", args.commit_message])
        except subprocess.CalledProcessError:
            print("Error: could not commit files")
            sys.exit(1)

    try:
        # Push the new branch to the remote repository
        if args.force:
            subprocess.run(["git", "push", "--force", "origin", args.branch_name])
        else:
            subprocess.run(["git", "push", "origin", args.branch_name])
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)


# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--branch_name", help="the name of the new branch (optional, defaults to the current branch)", default=None)
parser.add_argument("-f", "--force", help="force push", action='store_true')
parser.add_argument("commit_message", help="the commit message")
parser.add_argument("files", help="a list of files to commit (optional, defaults to all modified files)", nargs="*")
args = parser.parse_args()

# Create the new branch
create_branch(args)
