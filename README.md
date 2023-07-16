## Rlint

## Overview
Custom Python linter.

## Content
- [Installation](#installation)
- [Usage](#usage)
- [Config](#config)
- [Rules](#rules)
    - [R0001](#r0001)

## Installation
```bash
pip install git+https://github.com/ruauka/rlint-py.git
```

## Usage
Folders and files can be passed as arguments for verification using a **_relative path_**. You can specify an unlimited number of folders and files separated by a space.

Running a whole service check:
```bash
rlint .
```

Start checking a specific folder:
```bash
rlint folder
```

Start checking a specific file.py:
```bash
rlint folder/file.py
```

Start checking a specific folder and file.py:
```bash
rlint folder file.py
```

Start checking multiple folders and py-files:
```bash
rlint folder1 folder2 folder_n file1.py file2.py file_n.py
```

Start checking with **_cli keys_**.

Running a check specifying the path to the configuration file:
```bash
rlint folder file.py --config=path/to/pyproject.toml
```
## Config
To configure the linter, create a file `pyproject.toml` in the root of the checking application. In this case, the default path is `--config=pyproject.toml` and it is not required to specify it.

List of available configuration options:
```toml
[tool.rlint]
select = ["R0001"] # List of rules
exclude = ["folder", "file.py", "tests"] # Folders and files excluded from the check
format = "TEXT" # By default, the report format type is `TEXT`
```
- A folder with a `virtual environment` (`venv` or other names of this folder) is excluded by **_default_**, you do not need to add the folder name to the `exclude` option list.
- The `select` option is in development.
- The `format` option is in development.

## Rules

## R0001
Rule looks for `hardcode` in the source code.

Additional settings in `pyproject.toml`:
```toml
[tool.rlint.R0001]
threshold = 2
# The minimum threshold for the number of repetitions of the variable value.
# The default value is 2.
```
Example. 

`file.py`:
```python
a = "Hello world"
b = "Hello world"
```
This is 2 repetitions (but 1 double). The rule will work if `threshold = 2`:

```bash
file.py:1:4 R0001 Hardcode on variable with value: Hello world
file.py:2:4 R0001 Hardcode on variable with value: Hello world
```
The rule will not work if `threshold = 3`
