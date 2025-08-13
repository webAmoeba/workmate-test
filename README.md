# Workmate

Workmate is a tool for processing JSON log files and generating reports.
It supports multiple file processing, filtering records by date, and has an extensible report system.

## Features
- 📂 Process multiple log files in one run
- 📅 Filter records by date
- 📊 Several report formats (default, average, etc.)
- 🧩 Easily extensible — just add a new file to workmate/reports/ and it will be available as a report

## Requirements

- Python ≥ 3.13.5
- uv package manager

## Installation from repository

```bash
make install
```

## Installing into the system

```bash
make i
```

Add ~/.local/bin to your PATH if it’s not already there.
To add a directory to your PATH environment variable, you can use the following commands (replace .zshrc with the configuration file for your shell, e.g. .bashrc, .bash_profile, etc.):

```bash
cd
echo 'export PATH=$PATH:~/.local/bin' >> ~/.zshrc
source ~/.zshrc
```

## Usage

Show help:

```bash
workmate -h
```