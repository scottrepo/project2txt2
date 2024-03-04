# Project2txt - Project Code Aggregator

Project2txt is a Python script designed to aggregate all the source code files from a specified project into a single text file. This file is optimized for training or using as input into Large Language Models (LLMs) like ChatGPT. The script intelligently filters out non-source code files, removes comments, and formats the output to preserve the original structure and logic of the project code.

## Features

- Auto-Detection of Source Code: Automatically includes common source code files while excluding non-essential files (like .md, .csv, .pdf, etc.).
- Comment Removal: Strips line comments from the code to ensure clean, readable output.
- Customizable Filtering: Allows for custom configuration to include or exclude specific file types or directories.
- Interactive Mode: Offers an interactive mode for easy setup without the need to manually edit configuration files.
- Logging: Detailed logging of the script's operations, including files processed, skipped, and any errors encountered.

## Prerequisites

Before you begin, ensure you have the latest version of Python installed on your system. This script is compatible with Python 3.6 and above.

## Installation

1. Clone the Repository: First, clone this repository to your local machine using:

   ```
   git clone https://your-repository-url.git
   ```

2. Navigate to the Script Directory: Change into the cloned directory.

   ```
   cd path/to/project2txt
   ```

3. (Optional) Virtual Environment: It's a good practice to run Python projects in a virtual environment. Create and activate one with:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install Dependencies: This script uses the standard Python library, so no additional installations are required.

## Usage

You can run the script using the command line. The script offers both standard and interactive modes for flexibility.  Replace/use `python3` and `main.py` if applicable.

### Standard Mode

Run the script with the required parameters:

```
python project2txt.py --project_path "/path/to/your/project" --output_dir "/path/to/output/directory"
```

### Interactive Mode

If you run the script without any arguments, it will enter interactive mode, guiding you through the necessary inputs:

```
python project2txt.py
```

Follow the on-screen prompts to specify the project path and output directory.

1. Project Path: Enter the path to your project directory. Press Enter to use the current directory as the default.

2. Output Directory: Enter the directory where you want to save the output file. The default output directory is `output/your-project-name_combined_output`.

3. Configuration:
   - Press 'D' to use the default configuration, which includes the 10 most common programming languages and excludes common non-source code files and directories.
   - Press any other key to customize the configuration. You will be prompted to:
     - Enter file extensions to include and their corresponding comment symbols.
     - Enter additional file extensions to include and their corresponding comment symbols.
     - Enter additional folders or files to exclude.

The script will then process the project files based on the specified or default configuration and generate the output file.

## Configuration

The script uses a `DEFAULT_CONFIG` dictionary for the default configuration. This configuration includes:

- `include_patterns`: File extensions to include (default: 10 most common programming languages).
- `exclude_patterns`: Directories and files to exclude (default: common non-source code files and directories).
- `comment_patterns`: Comment symbols for each file extension.
- `output_format`: Delimiter format for separating files in the output.

You can modify the `DEFAULT_CONFIG` dictionary in the script to adjust the default configuration according to your needs.

## Logs

The script generates logs to the console, logging detailed information about its execution. Consult this log for troubleshooting or to review the script's actions.

## Examples

Here are a few examples of how to use the script, replace project2txt.py with main.py in this use case:

1. Process a project using the default configuration:

   ```
   python project2txt.py --project_path "/path/to/your/project" --output_dir "/path/to/output/directory"
   ```

2. Process a project using interactive mode:

   ```
   python project2txt.py
   ```

   Follow the on-screen prompts to enter the project path, output directory, and configuration options.

3. Process a project using a custom configuration:

   ```
   python project2txt.py --project_path "/path/to/your/project" --output_dir "/path/to/output/directory"
   ```

   In interactive mode, choose to customize the configuration and enter the desired file extensions, comment symbols, and additional exclusions.

## Troubleshooting

- If the script fails to process certain files, ensure that you have the necessary permissions to read and write files in the specified directories.

- If the output file is not generated, check the console logs for any error messages and ensure that the output directory exists and has write permissions.

- If the script is not behaving as expected, review the configuration settings and make sure they align with your project's structure and requirements.

## Contributing

Contributions to Project2txt are welcome! If you encounter any issues or have suggestions for improvements, please create an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
