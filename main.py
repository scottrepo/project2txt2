# Import modules
import argparse
import json
import os
import re
from enum import Enum


class FileExtension(Enum):
    """Enum for file extensions."""
    PY = ".py"
    JS = ".js"
    JAVA = ".java"
    CPP = ".cpp"
    C = ".c"
    CS = ".cs"
    PHP = ".php"
    RUBY = ".rb"
    GO = ".go"
    SWIFT = ".swift"


DEFAULT_CONFIG = {
    "include_patterns": [
        f"{ext.value}$" for ext in [
            FileExtension.PY,
            FileExtension.JS,
            FileExtension.JAVA,
            FileExtension.CPP,
            FileExtension.C,
            FileExtension.CS,
            FileExtension.PHP,
            FileExtension.RUBY,
            FileExtension.GO,
            FileExtension.SWIFT
        ]
    ],
    "exclude_patterns": [
        r"\.git/", r"\.svn/", r"\.hg/",  # Version control directories
        r"node_modules/", r"bower_components/", r"venv/", r"\.venv/",  # Package/dependency directories
        r"bin/", r"obj/", r"dist/", r"build/", r"\.exe$", r"\.dll$", r"\.so$", r"\.o$",  # Build outputs
        r"\.env$", r".*.config", r"\.DS_Store", r"Thumbs.db",  # Configs and secrets
        r"\.md$", r"\.txt$", r"\.pdf$", r"\.csv$",  # Docs and non-code files
        r"test/", r"tests/",  # Test directories
        r"\.tmp$", r"\.cache", r"\.pyc", r"__pycache__/",  # Temporary/cache files
        r"\.log",  # Log files
        r"docs/", r"examples/", r"samples/",  # Specific project directories
        r"^\.",  # Hidden files and folders
        r"/\."  # Hidden files and folders inside subdirectories
    ],
    "comment_patterns": {
        ".py": "#",
        ".js": "//",
        ".java": "//",
        ".cpp": "//",
        ".c": "//",
        ".cs": "//",
        ".php": "//",
        ".rb": "#",
        ".go": "//",
        ".swift": "//"
    },
    "output_format": {
        "delimiter": "\n<<<FILENAME:{file_path}>>>\n"
    }
}


# Function to check if the file should be excluded
def should_exclude_file(file_path, config):
    return any(re.search(pattern, file_path) for pattern in config["exclude_patterns"])


# Function to check if the file should be included
def should_include_file(file_path, config):
    return any(re.search(pattern, file_path) for pattern in config["include_patterns"])


def load_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}. Using default settings.")
        return DEFAULT_CONFIG
    except json.JSONDecodeError:
        print("Error decoding JSON configuration file. Using default settings.")
        return DEFAULT_CONFIG


def remove_comments(file_content, comment_pattern):
    clean_content = re.sub(f"{comment_pattern}.*", "", file_content)
    return clean_content


def process_file(file_path, config, output_file):
    # Check if the provided path is actually a file
    if not os.path.isfile(file_path):
        print(f"Invalid file path: {file_path}")
        return

    if should_exclude_file(file_path, config):
        print(f"Skipping {file_path}")
        return

    if should_include_file(file_path, config):
        file_extension = os.path.splitext(file_path)[1]
        comment_pattern = config["comment_patterns"].get(file_extension)

        file_content = read_file(file_path)
        if file_content is not None:
            clean_content = remove_comments_if_needed(file_content, comment_pattern)
            write_to_output_file(output_file, file_path, clean_content, config["output_format"]["delimiter"])


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except PermissionError:
        print(f"Permission denied to read {file_path}")
        return None


def remove_comments_if_needed(file_content, comment_pattern):
    if comment_pattern:
        clean_content = re.sub(f"{comment_pattern}.*", "", file_content)
        return os.linesep.join([s for s in clean_content.splitlines() if s.strip()])
    else:
        return os.linesep.join([s for s in file_content.splitlines() if s.strip()])


def write_to_output_file(output_file, file_path, clean_content, delimiter):
    formatted_delimiter = delimiter.format(file_path=file_path)
    with open(output_file, 'a') as out_file:
        out_file.write(formatted_delimiter + clean_content + "\n")


def get_project_name_from_path(project_path):
    return os.path.basename(os.path.normpath(project_path))


def process_project(project_path, output_file_path, config):
    with open(output_file_path, 'w'):
        pass  # Ensure the output file is empty before starting

    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, config, output_file_path)

    print(f"Project processing complete. Output saved to {output_file_path}")


def generate_config_interactively():
    print("Interactive Configuration Generator")
    config = DEFAULT_CONFIG.copy()

    # Prompt the user to use default configuration or customize
    use_default = input("Do you want to use the default configuration? (Y/N): ").strip().lower()
    if use_default == 'n':
        config["include_patterns"] = []
        config["exclude_patterns"] = []
        config["comment_patterns"] = {}

        # Adding include patterns interactively
        while True:
            pattern = input("Enter a file extension to include (e.g., .py) or press Enter to finish: ").strip()
            if not pattern:
                break
            comment = input(f"Enter the comment symbol for {pattern} (e.g., #): ").strip()
            config["include_patterns"].append(pattern + "$")  # Ensuring it's treated as an extension
            config["comment_patterns"][pattern] = comment

    # Adding additional include patterns interactively
    print("\nAdditional Include Patterns")
    while True:
        pattern = input("Enter an additional file extension to include (e.g., .py) or press Enter to finish: ").strip()
        if not pattern:
            break
        comment = input(f"Enter the comment symbol for {pattern} (e.g., #): ").strip()
        config["include_patterns"].append(pattern + "$")  # Ensuring it's treated as an extension
        config["comment_patterns"][pattern] = comment

    # Adding additional exclude patterns interactively
    print("\nAdditional Exclude Patterns")
    while True:
        folder = input(
            "Enter an additional folder or file to exclude (e.g., tests/) or press Enter to finish: ").strip()
        if not folder:
            break
        config["exclude_patterns"].append(folder)

    return config


def check_for_interactive_mode(args):
    # Assume interactive mode if all arguments are None (indicating they were not provided)
    return all(value is None for value in vars(args).values())


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process project files into a single text file for LLM training.")
    parser.add_argument("--project_path", help="Path to the project directory", nargs='?', const='', default=None)
    parser.add_argument("--output_dir", help="Directory to save the output file", nargs='?', const='', default=None)
    parser.add_argument("--config", help="Path to configuration file", nargs='?', const='', default="config.json")
    return parser.parse_args()


def main():
    args = parse_arguments()
    # Determine if the script is in interactive mode based on the presence of arguments
    interactive_mode = args.project_path is None and args.output_dir is None

    if interactive_mode:
        print("Entering interactive mode...")
        # Interactive prompts for project path and output directory
        args.project_path = input("Enter the path to your project: ").strip() or '.'
        default_output_dir = os.path.join("output",
                                          os.path.basename(os.path.normpath(args.project_path)) + "_combined_output")
        args.output_dir = input(f"Enter the output directory [{default_output_dir}]: ").strip() or default_output_dir

        # Ensuring the output directory exists
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)

        # Interactive Configuration Choice
        use_default_config = input(
            "Press 'D' to use the default configuration, or any other key to customize: ").lower() == 'd'
        if use_default_config:
            config = DEFAULT_CONFIG
            print("Using default configuration.")
        else:
            config = generate_config_interactively()
            # Optionally save the generated config to a file
            with open(args.config, 'w') as config_file:
                json.dump(config, config_file, indent=4)
    else:
        # Non-interactive mode configuration loading
        if os.path.exists(args.config):
            config = load_config(args.config)
        else:
            config = DEFAULT_CONFIG

    # Proceed with processing using the determined or default configuration
    output_file_name = os.path.basename(os.path.normpath(args.project_path)) + ".txt"
    output_file_path = os.path.join(args.output_dir, output_file_name)

    process_project(args.project_path, output_file_path, config)

    print(f"Project processing complete. Output saved to {output_file_path}")


if __name__ == "__main__":
    main()
