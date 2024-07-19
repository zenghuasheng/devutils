import os
import subprocess


def run_command(command, cwd=None):
    current_env = os.environ.copy()
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True, env=current_env)
    print(f"Running command: {command}")
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
        exit(1)
    return result.stdout.strip()


def update_repository(repo_path, branch, commit_message, dependency_repo=None, dependency_repo_commit_id=None):
    print(f"Updating repository at {repo_path}")

    # Fetch all branches and tags
    run_command("git fetch --all", cwd=repo_path)

    # Check if the branch exists
    branches = run_command("git branch -a", cwd=repo_path).split('\n')
    branch_exists = any(branch.strip() == f"remotes/origin/{branch}" or branch.strip() == branch for branch in branches)

    if not branch_exists:
        print(f"Branch {branch} does not exist in repository {repo_path}")
        return None

    # Change to the specified branch
    run_command(f"git checkout {branch}", cwd=repo_path)

    if dependency_repo is not None:
        update_dependency_in_go_mod(repo_path, dependency_repo, dependency_repo_commit_id)

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


def update_dependency_in_go_mod(repo_path, dependency, commit_id_common):
    # repo_path_project = "/Users/xhs/go/src/github.com/bangwork/ones-project-api"
    if commit_id_common is not None or not is_latest_commit_in_go_mod(
            # "github.com/bangwork/ones-api-biz-common"
            repo_path, dependency, commit_id_common):
        run_command(f"go get {dependency}@{commit_id_common}", cwd=repo_path)
    # 执行 go mod tidy
    run_command("go mod tidy", cwd=repo_path)
    run_command("CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /tmp/", cwd=repo_path)


def main(branch, commit_message):
    # Update ones-api-biz-common repository
    repo_path_common = "/Users/xhs/go/src/github.com/bangwork/ones-api-biz-common"
    commit_id_common = update_repository(repo_path_common, branch, commit_message)

    # Update ones-project-api repository
    repo_path_project = "/Users/xhs/go/src/github.com/bangwork/ones-project-api"
    dependency_repo = "github.com/bangwork/ones-api-biz-common"
    dependency_repo_commit_id = commit_id_common
    commit_id_project = update_repository(repo_path_project, branch, commit_message, dependency_repo,
                                          dependency_repo_commit_id)
    # Update bang-api-gomod repository
    repo_path_bang = "/Users/xhs/go/src/github.com/bangwork/bang-api-gomod"
    dependency_repo = "github.com/bangwork/ones-project-api"
    dependency_repo_commit_id = commit_id_project
    update_repository(repo_path_bang, branch, commit_message, dependency_repo, dependency_repo_commit_id)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python update_repos.py <branch> <commit_message>")
        exit(1)

    branch = sys.argv[1]
    commit_message = sys.argv[2]

    main(branch, commit_message)
