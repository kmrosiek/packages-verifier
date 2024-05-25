import os
import yaml
import networkx as nx
import matplotlib.pyplot as plt

# Function to parse a YAML file
def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to find all pubspec.yaml files in the given directory
def find_pubspec_files(base_dir):
    pubspec_files = []
    for root, dirs, files in os.walk(base_dir):
        if 'pubspec.yaml' in files:
            pubspec_files.append(os.path.join(root, 'pubspec.yaml'))
    return pubspec_files

# Function to extract dependencies from a pubspec.yaml file
def extract_dependencies(file_path):
    data = parse_yaml(file_path)
    dependencies = data.get('dependencies', {})
    dev_dependencies = data.get('dev_dependencies', {})
    all_dependencies = {**dependencies, **dev_dependencies}
    return {k: v for k, v in all_dependencies.items() if isinstance(v, dict) and 'path' in v}

# Function to build the dependency graph and check for forbidden dependencies
def build_dependency_graph(base_dir, packages_without_deps, restricted_packages):
    G = nx.DiGraph()
    pubspec_files = find_pubspec_files(base_dir)
    base_package_name = os.path.basename(base_dir.rstrip('/'))

    for pubspec_file in pubspec_files:
        package_name = os.path.basename(os.path.dirname(pubspec_file))
        dependencies = extract_dependencies(pubspec_file)

        # Check for forbidden dependencies
        if package_name in packages_without_deps and dependencies:
            print(f"Warning: Package '{package_name}' should not have dependencies but has:")
            for dep_name, dep_info in dependencies.items():
                print(f"  - {dep_name}: {dep_info}")

        G.add_node(package_name)
        for dep_name, dep_info in dependencies.items():
            dep_path = dep_info['path']
            dep_package_name = os.path.basename(os.path.normpath(dep_path))
            G.add_edge(package_name, dep_package_name)

            # Check for restricted package imports
            if dep_package_name in restricted_packages and package_name != base_package_name:
                print(f"Warning: Package '{package_name}' should not import restricted package '{dep_package_name}'")

    # Check for circular dependencies of length 2
    checked_pairs = set()
    for u, v in G.edges():
        if G.has_edge(v, u) and (v, u) not in checked_pairs:
            print(f"Warning: Circular dependency found between '{u}' and '{v}'")
            checked_pairs.add((u, v))
            checked_pairs.add((v, u))

    return G

# Function to visualize the dependency graph
def visualize_graph(G):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', arrows=True, arrowsize=20)
    plt.show()


# Main function to build and visualize the dependency graph
def main():
    base_dir = '../github_viewer/'  # Change this to your base directory
    packages_without_deps = ['common']  # List of packages that should not have dependencies
    restricted_packages = ['firebase_repository']  # List of packages that should only be imported by the main package
    G = build_dependency_graph(base_dir, packages_without_deps, restricted_packages)
    visualize_graph(G)

if __name__ == "__main__":
    main()
