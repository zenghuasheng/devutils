import subprocess
import os


def find_init_func(directory):
    init_func_files = []
    find_command = f"find {directory} -type f -name '*.go' -exec grep -l 'func init()' {{}} +"
    result = subprocess.run(find_command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output = result.stdout.strip()
        init_func_files = output.split('\n')
        init_func_files = [os.path.relpath(file, directory) for file in init_func_files]
    return init_func_files


def search_reference(init_func_files, *directories):
    for init_file in init_func_files:
        found_reference = False
        for directory in directories:
            search_command = f"find {directory} -type f -exec grep -q '/{init_file[:-3]}' {{}} \\; -print"
            print(search_command)
            result = subprocess.run(search_command, shell=True, capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip() != "":
                found_reference = True
                break
        if not found_reference:
            print(f"No reference found for init function in {init_file}")


if __name__ == "__main__":
    base_directory = "/Users/xhs/go/src/github.com/bangwork/ones-project-api"
    search_directories = [
        base_directory,
        "/Users/xhs/go/src/github.com/bangwork/bang-api-gomod",
        # Add more directories here if needed
    ]

    init_func_files = find_init_func(base_directory)
    search_reference(init_func_files, *search_directories)
