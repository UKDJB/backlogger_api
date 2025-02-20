import os

EXCLUDED_FOLDERS = {".git", ".venv", "__pycache__",
                    ".pytest_cache"}  # Add more if needed


# Start indent at 1 for leading tab
def generate_folder_structure(directory, indent=1):
    """ Recursively generates an indented folder structure using only tabs. """
    try:
        items = sorted(os.listdir(directory))  # Get sorted list of items
    except PermissionError:
        return "  " * indent + "[ACCESS DENIED]\n"  # Handle permission errors

    structure = ""

    for item in items:
        path = os.path.join(directory, item)
        if item in EXCLUDED_FOLDERS or item.startswith('.'):
            continue  # Skip unwanted directories

        prefix = "  " * indent  # Indentation using tabs
        if os.path.isdir(path):
            structure += f"{prefix}{item}/\n"  # Add slash to indicate a folder
            structure += generate_folder_structure(path, indent + 1)
        else:
            structure += f"{prefix}{item}\n"  # Just list the file

    return structure


def save_structure_to_file(root_directory, output_file):
    """ Saves the folder structure to a text file with a leading tab on all rows. """
    if not os.path.exists(root_directory):
        print(f"Error: Directory '{root_directory}' does not exist.")
        return

    # Get only the last part of the root path (e.g., "backlogger_api" instead of "/Users/davidbrown/backlogger_api")
    root_name = os.path.basename(root_directory)
    structure = generate_folder_structure(root_directory)

    with open(output_file, "w", encoding="utf-8") as file:
        # Add a leading tab to the root directory
        file.write(f"\t{root_name}/\n{structure}")


if __name__ == "__main__":
    # Change this to your actual folder path
    root_folder = "/Users/davidbrown/backlogger_api"
    output_file = "_documentation/tree_source.txt"

    save_structure_to_file(root_folder, output_file)
    print(f"Cleaned folder structure saved to {output_file}")
