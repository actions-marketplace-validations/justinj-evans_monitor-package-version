from github_interaction import add_text_to_commit, download_requirements_to_json
from requirements import check_requirements, format_requirements_as_text
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='action.yml arguments')
    parser.add_argument('--token', type=str, help='GitHub token')
    parser.add_argument('--repo', type=str, help='Repository name')
    parser.add_argument('--pull_number', type=str, help='Pull request number')
    parser.add_argument('--commit_sha', type=str, help='Commit SHA')
    parser.add_argument('--existing_sha', type=str, help='Existing SHA')
    parser.add_argument('--upgrade', type=bool, help='Whether to upgrade')
    parser.add_argument('--downgrade', type=bool, help='Whether to downgrade')
    parser.add_argument('--new_package', type=bool, help='Whether it is a new package')
    args = parser.parse_args()
    return args

def user_notification():
    """Main driver of Github Action
    """

    # get user input passed by args
    args = parse_args()

    # check if user input has been specified
    if args.new_package or args.upgrade or args.downgrade:

        user_input = {
            'new_packages': args.new_package,
            'upgraded_packages': args.upgrade,
            'downgraded_packages': args.downgrade
            }
    
        # extract requirements
        existing_requirements = download_requirements_to_json(repo=args.repo, commit=args.existing_sha, path="requirements.txt")
        new_requirements = download_requirements_to_json(repo=args.repo, commit=args.commit_sha, path="requirements.txt")

        # compare user's committed requirements from previous commit
        compare_requirements = check_requirements(existing_requirements=existing_requirements, new_requirements=new_requirements)

        # based on user input, adjust formatted text
        requirements_text = format_requirements_as_text(user_input=user_input, data=compare_requirements)

        # only add commit if diff found and message formatted
        if requirements_text:
            # add formatted requirement check to commit message
            add_text_to_commit(token=args.token, repo_name=args.repo,
                            commit_sha=args.commit_sha, additional_text=requirements_text)
        else:
            print("Github Action 'Monitor Package Version' found no new, upgraded, or downgraded pacakges")

if __name__ == "__main__":

    user_notification()