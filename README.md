# Dependency Management and Analysis Scripts

This repository contains two Python scripts designed for managing and analyzing package dependencies within a project that uses `pubspec.yaml` files (commonly found in Dart/Flutter projects).

## Script 1: Version Checker and Updater

This script (`version_checker.py`) checks and updates package versions in `pubspec.yaml` files according to a reference version file.

### Features

- **Read Reference Versions:** Reads package versions from a reference file (`pubspec-source.yaml`).
- **Update Versions:** Updates the versions in `pubspec.yaml` files to match the reference versions.
- **Interactive Prompt:** Prompts the user for confirmation before updating versions (can be skipped with a flag).
- **Recursive Search:** Searches for `pubspec.yaml` files recursively within the specified directory.

### How to Use

1. **Prepare the Reference File:** Create a file named `pubspec-source.yaml` with the following structure:
   ```yaml
   name: package_versions
   publish_to: none
   environment:
      sdk: ">=3.3.4 <4.0.0"
   dependencies:
     package_name1: version1
     package_name2: version2
     ...
   
Run the Script:
```bash
python3 version_checker.py [-y]
```
The -y flag can be used to automatically update versions without prompting for confirmation.
Example Usage
```bash
python3 version_checker.py -y
```

## Script 2: Dependency Graph Builder and Analyzer
This script (dependency_graph_analyzer.py) builds and visualizes a dependency graph from pubspec.yaml files. It also checks for forbidden dependencies and circular dependencies.

### Features
- Parse Dependencies: Extracts dependencies from pubspec.yaml files.
- Build Dependency Graph: Constructs a directed graph of package dependencies.
- Forbidden Dependencies Check: Warns if certain packages have dependencies or import restricted packages.
- Circular Dependencies Check: Detects and warns about circular dependencies of length 2.
- Visualization: Visualizes the dependency graph using Matplotlib.

### How to Use
1. Set Up Base Directory and Restrictions: Modify the main() function to set your base directory, packages without dependencies, and restricted packages.
```python
base_dir = '../your_project_directory/' # Change this to your base directory
packages_without_deps = ['common'] # List of packages that should not have dependencies
restricted_packages = ['firebase_repository'] # List of packages that should only be imported by the main package
```

Run the Script:
```bash
python dependency_graph_analyzer.py
```bash

Example Usage
```bash
python3 dependency_graph_analyzer.py
```

### Visualization
The dependency graph will be visualized using Matplotlib, showing the relationships between packages in a clear graphical format.

### Dependencies
Ensure you have the following Python packages installed:
```bash
pip install pyyaml networkx matplotlib
```
### Conclusion
These scripts provide an automated way to manage and analyze dependencies in Dart/Flutter projects, helping maintain consistency in package versions and ensuring a clean and understandable dependency structure.
