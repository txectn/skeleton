import os


def print_directory_structure(
    root_dir,
    indent=0,
    ignore_folders=None,
    ignore_files=None,
):
    if not os.path.exists(root_dir):
        print(f"Error: The folder '{root_dir}' does not exist.")
        return

    ignore_folders = ignore_folders or []
    ignore_files = ignore_files or []

    items = os.listdir(root_dir)

    # Remove ignored items
    items = [
        item
        for item in items
        if item not in ignore_folders
        and item not in ignore_files
    ]

    for i, item in enumerate(items):
        item_path = os.path.join(root_dir, item)
        is_last = i == len(items) - 1

        prefix = '└── ' if is_last else '├── '
        line = '    ' * indent + prefix + item

        print(line)

        if os.path.isdir(item_path):
            print_directory_structure(
                item_path,
                indent + 1,
                ignore_folders,
                ignore_files,
            )


# Automatically find folder relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.join(script_dir, "./backend/products/serializers")

# Things to ignore
ignore_folders = [
    "__pycache__",
    ".git",
    "migrations",
]

ignore_files = [
    "__init__.py",
    ".gitignore",
    "test.py",
]

# Print directory structure
print(root_folder)

print_directory_structure(
    root_folder,
    ignore_folders=ignore_folders,
    ignore_files=ignore_files,
)