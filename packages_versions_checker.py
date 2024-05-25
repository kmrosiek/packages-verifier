import os
import re
import argparse

def read_versions(versions_file):
    versions_data = {}
    with open(versions_file, 'r') as f:
        start_line = find_line_where_packages_start(f)
        f.seek(0)
        lines = f.readlines()[start_line:]
        for line in lines:
            package, version = line.strip().split(': ')
            versions_data[package.strip()] = version.strip()
    return versions_data

def find_line_where_packages_start(file):
    for line_number, line in enumerate(file, 1):
            if 'dependencies:' in line:
                return line_number
    return -1

def update_versions(pubspec_path, versions_data, skip_prompt):
    modified = False
    updated_content = []
    with open(pubspec_path, 'r') as f:
        for line in f:
            for package, version in versions_data.items():
                pattern = re.compile(f"^{package}:")
                if re.match(pattern, line.strip()):
                    if f"  {package}: {version}\n" != line:
                        current_version = line.split(': ')[-1].strip()
                        print(f"Mismatched package '{package}' version: Current version '{current_version}' | Expected version '{versions_data[package]}' in file: {pubspec_path}")
                        choice = 'y' if skip_prompt else input("Do you want to modify it? (y/n): ")
                        if choice.lower() in ['yes', 'y']:
                            print("Modifying...")
                            line = f"  {package}: {version}\n"
                            modified = True
                        else:
                            print('Skipping...')
            updated_content.append(line)

    if modified:
        with open(pubspec_path, 'w') as f:
            f.writelines(updated_content)
    return modified

def check_versions(versions_file, search_path, skip_prompt):
    versions_data = read_versions(versions_file)

    for root, dirs, files in os.walk(search_path):
        if "packages_versions" in root:
            continue
        for file in files:
            if file == 'pubspec.yaml':
                pubspec_path = os.path.join(root, file)
                print(f"Running check for {pubspec_path}")
                modified = update_versions(pubspec_path, versions_data, skip_prompt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Checks and updates packages versions in pubspec.yaml files.')
    parser.add_argument('-y', action='store_true', help='Automatically update versions without prompting')
    args = parser.parse_args()

    print(f"{os.path.dirname(__file__)}/")
    check_versions(f"{os.path.dirname(__file__)}/pubspec-source.yaml", '.', args.y)
