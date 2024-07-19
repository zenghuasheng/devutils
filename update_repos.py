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


def update_repository(repo_path, branch, commit_message):
    print(f"Updating repository at {repo_path}")

    # Change to the specified branch
    run_command(f"git checkout {branch}", cwd=repo_path)

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


def main(branch, commit_message):
    # Update ones-api-biz-common repository
    repo_path_common = "/Users/xhs/go/src/github.com/bangwork/ones-api-biz-common"
    commit_id_common = update_repository(repo_path_common, branch, commit_message)

    # Update ones-project-api repository
    repo_path_project = "/Users/xhs/go/src/github.com/bangwork/ones-project-api"
    if not is_latest_commit_in_go_mod(repo_path_project, "github.com/bangwork/ones-api-biz-common", commit_id_common):
        run_command(f"go get github.com/bangwork/ones-api-biz-common@{commit_id_common}", cwd=repo_path_project)

    # 执行 go mod tidy
    run_command("go mod tidy", cwd=repo_path_project)
    run_command("CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /tmp/", cwd=repo_path_project)
    commit_id_project = update_repository(repo_path_project, branch, commit_message)

    # Update bang-api-gomod repository
    repo_path_bang = "/Users/xhs/go/src/github.com/bangwork/bang-api-gomod"
    if not is_latest_commit_in_go_mod(repo_path_bang, "github.com/bangwork/ones-project-api", commit_id_project):
        run_command(f"go get github.com/bangwork/ones-project-api@{commit_id_project}", cwd=repo_path_bang)

    # 执行 go mod tidy
    run_command("go mod tidy", cwd=repo_path_bang)
    run_command("CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /tmp/", cwd=repo_path_bang)
    update_repository(repo_path_bang, branch, commit_message)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python update_repos.py <branch> <commit_message>")
        exit(1)

    branch = sys.argv[1]
    commit_message = sys.argv[2]

    main(branch, commit_message)
