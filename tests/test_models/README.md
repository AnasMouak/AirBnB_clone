# 0x00. AirBnB clone - The console

## Introduction
This project is part of the AirBnB clone project. The console is a command interpreter designed to manage objects for the AirBnB project. It allows for creating, updating, and managing objects via a simple command-line interface.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Console Command Reference](#console-command-reference)
- [FileStorage Functionality](#filestorage-functionality)
- [Examples](#examples)
  - [Interactive Mode Example](#interactive-mode-example)
  - [Non-Interactive Mode Example](#non-interactive-mode-example)
- [Dependencies](#dependencies)
- [Contributors](#contributors)

## Installation
To use this project, clone the repo to your local machine:
```bash
https://github.com/AnasMouak/AirBnB_clone
```

## Usage
The console can be run both in interactive mode and non-interactive mode. Here's how you can use it in both modes:

### Interactive Mode
Run the console in interactive mode:
```bash
./console.py
```
You can then enter commands directly into the console.

### Non-Interactive Mode
Run the console in non-interactive mode by piping commands into it from a shell:
```bash
echo "your-command-here" | ./console.py
```

## Console Command Reference
Detailed explanations of all console commands are provided below.

| Command | Description | Usage | Example |
|---------|-------------|-------|---------|
| `quit` | Exits the console. | `quit` | `quit` |
| `EOF` | Exits the console with EOF signal (Ctrl+D). | `EOF` | `EOF` |
| `create` | Creates a new instance of a given class. | `create <class name>` | `create User` |
| `show` | Shows an instance based on the class name and id. | `show <class name> <id>` | `show User 1234-1234-1234` |
| `destroy` | Deletes an instance based on the class name and id. | `destroy <class name> <id>` | `destroy User 1234-1234-1234` |
| `all` | Shows all instances of a class or all classes if not specified. | `all` or `all <class name>` | `all User` |
| `update` | Updates an instance by adding or updating an attribute. | `update <class name> <id> <attribute name> "<attribute value>"` | `update User 1234-1234-1234 email "a@b.com"` |
| `count` | Counts instances of a specific class. | `count <class name>` | `count User` |

## FileStorage Functionality
Below is a brief overview of the `FileStorage` class methods and their functionality.

| Method | Description |
|--------|-------------|
| `all()` | Returns the dictionary of all saved objects. |
| `new(obj)` | Adds an object to the storage dictionary. |
| `save()` | Serializes the storage dictionary to a JSON file. |
| `reload()` | Deserializes the JSON file to the storage dictionary, if the file exists. |

## Examples

### Interactive Mode Example
Here's an example of using the console in interactive mode, including the help command for `destroy`:

```bash
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

(hbnb) help destroy

        Deletes an instance based on the class name and id.
        Usage: destroy <class name> <id>
        Example: destroy User 1234-1234-1234

(hbnb)
```

### Non-Interactive Mode Example
Here's how you might use the console in non-interactive mode to create a new `User`:

```bash
echo "create User" | ./console.py
```

This will output the ID of the newly created `User` instance.

## Dependencies
This project requires Python 3.7 or later.

## Contributors
- Yassine Mtejjal
- Anas Mouak
