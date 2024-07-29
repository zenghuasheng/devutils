import argparse
import os
import subprocess

import yaml


def run_command(command, cwd=None):
    current_env = os.environ.copy()
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True, env=current_env)
    print(f"Running command: {command}")
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
        exit(1)
    return result.stdout.strip()


def update_repository(repo_path, branch, commit_message, dependencies=None):
    print(f"Updating repository at {repo_path}")

    # Fetch all branches and tags
    run_command("git fetch origin", cwd=repo_path)

    # Check if the branch exists
    branches = run_command("git branch -a", cwd=repo_path).split('\n')
    # branch_exists = any(branch.strip() == f"remotes/origin/{branch}" or branch.strip() == branch for branch in branches)
    branch_exists = False
    for b in branches:
        if b.strip() == f"remotes/origin/{branch}" or b.strip() == f"* {branch}" or b.strip() == branch:
            branch_exists = True
            break

    if not branch_exists:
        print(f"Branch {branch} does not exist in repository {repo_path}")
        return None

    # Change to the specified branch
    run_command(f"git checkout {branch}", cwd=repo_path)

    # git pull origin branch
    run_command(f"git pull origin {branch}", cwd=repo_path)

    if dependencies:
        for dependency in dependencies:
            dependency_repo = f"github.com/bangwork/{dependency['name']}"
            update_dependency_in_go_mod(repo_path, dependency_repo, dependency['commit_id'])

    # Check if the working directory is clean
    status = run_command("git status --porcelain", cwd=repo_path)
    if status == "":
        # Working directory is clean, get the latest commit ID
        commit_id = run_command("git log -1 --pretty=format:%H", cwd=repo_path)
        print(f"Latest commit ID: {commit_id}")
        return commit_id

    # Stage all changes
    run_command("git add .", cwd=repo_path)

    # Commit changes
    run_command(f"git commit -m \"{commit_message}\"", cwd=repo_path)

    # Push changes
    run_command(f"git push origin {branch}", cwd=repo_path)

    # Get the latest commit ID
    commit_id = run_command("git log -1 --pretty=format:%H", cwd=repo_path)
    print(f"Latest commit ID: {commit_id}")

    return commit_id


def is_latest_commit_in_go_mod(repo_path, dependency, commit_id):
    go_mod_content = run_command("cat go.mod", cwd=repo_path)
    dependency_line = f"\t{dependency} v"
    for line in go_mod_content.split('\n'):
        if line.startswith(dependency_line):
            parts = line.split('-')
            if parts[-1] == commit_id[:12]:  # Check if the commit ID matches the short format
                return True
    return False


def update_dependency_in_go_mod(repo_path, dependency, commit_id):
    if commit_id is not None:
        if not is_latest_commit_in_go_mod(repo_path, dependency, commit_id):
            print(f"Updating dependency {dependency} to commit ID {commit_id} in go.mod")
            run_command(f"go get {dependency}@{commit_id}", cwd=repo_path)
    # 执行 go mod tidy
    run_command("go mod tidy", cwd=repo_path)

    if os.path.exists(os.path.join(repo_path, 'main.go')):
        run_command("CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /tmp/", cwd=repo_path)


def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def main(branch, commit_message, config_path='repos.yaml'):
    config = load_config(config_path)
    repositories = config['repositories']

    commit_ids = {}
    for repo_name, repo_info in repositories.items():
        repo_path = repo_info['path']
        dependencies = repo_info.get('dependencies', [])

        for dependency in dependencies:
            dependency_name = dependency['name']
            dependency['commit_id'] = commit_ids.get(dependency_name)

        commit_id = update_repository(repo_path, branch, commit_message, dependencies)
        if commit_id:
            commit_ids[repo_name] = commit_id


def parse_command_line_args():
    parser = argparse.ArgumentParser(description="cascading update go repo dependency version")
    parser.add_argument("branch", help="branch to update")
    parser.add_argument("commit_message", help="commit message for the update")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_command_line_args()
    # config_path 和 update_repos.py 在同一目录下
    config_path = os.path.join(os.path.dirname(__file__), 'repos.yaml')
    main(args.branch, args.commit_message, config_path=config_path)
