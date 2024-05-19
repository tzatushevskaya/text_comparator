## Task: Create a Text Editor with Difference Highlighting

**Objective**: Develop a Python application using PySide6 to create a text editor widget capable of displaying differences between two source code files. The editor should have syntax highlighting, line numbers, and visually highlight added and removed lines.

**Requirements**:
- Utilize PySide6 for the GUI components.
- Implement syntax highlighting for the source code.
- Display line numbers for reference.
- Highlight added lines in green and removed lines in red to visually indicate differences between the two files.
- Ensure the widget looks aesthetically pleasing.

**Implementation Steps**:
1. Create a custom widget subclassing `QPlainTextEdit` for the text editor.
2. Implement syntax highlighting for the source code using `QSyntaxHighlighter`.
3. Implement a method to highlight differences between two text strings, indicating additions and removals.
4. Create a main widget class to contain the custom text editor widget.
5. Test the application with sample text files to verify the difference highlighting functionality.

**Expected Output**: 
Upon execution, the application should launch a GUI window displaying the custom text editor widget 
with syntax highlighting and difference highlighting for the provided sample text files.


## Prerequisites

This project requires a Linux operating system to run.
In order to run it inside the docker container docker must be installed.

## Installation

1. Clone the repository to your local machine.
    ```bash
    git clone https://github.com/tzatushevskaya/TextComparator.git
    ```
2. Navigate to the project directory.
    ```bash
    cd ./TextComparator
    ```

It's recommended to run this project in a virtual environment to manage dependencies cleanly. 
You can use tools like `venv` or `micromamba` to create a virtual environment.

### Using micromamba

If you have micromamba installed, you can create a virtual environment and install dependencies like this:

```bash
# Create a new virtual environment
micromamba create -n myenv python=3.12

# Activate the virtual environment
micromamba activate myenv

# Install project dependencies
pip install poetry
poetry install
```

### Using venv

If you prefer using venv, you can create and activate a virtual environment like this:

```bash
# Create a new virtual environment
python -m venv myenv

# Activate the virtual environment 
source myenv/bin/activate

# Install project dependencies
pip install poetry
poetry install
```

### Using docker

Build a docker image:
```bash
docker build -f <image_name>:<tag> -f Dockerfile .
```

Run the container (demo mode):
```bash
docker run --device /dev/snd <image_name>:<tag>
```

## Running the Application

### Without Parameters (Demo Mode)
Run the app without parameters (it will process the existing text samples):
```bash
python app.py
```

### With Parameters
Run the app with the desired parameters:
```bash
python app.py <path_to_text_file1> <path_to_text_file2>
```
Replace `<path_to_text_file1>` and `<path_to_text_file2>` with the path to the actual text files you want to compare.

## Testing the Application
Execute the unit tests:
```bash
python -m unittest -v
```
