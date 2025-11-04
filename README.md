# ezbash

**The natural language way of interacting with a Linux terminal.**

Skip the man pages. Operate the terminal in natural language, and ezbash generates the exact Linux command you need. Review it, then run it.

## Overview

ezbash is a command-line utility that translates natural language descriptions into proper Linux commands using LLM (Large Language Model) technology. It includes a crucial human-review step before execution, ensuring safety and control.

## Features

- 🗣️ Natural language command generation
- ✅ Human-in-the-loop review before execution
- 🔒 Safe by design - no commands run without approval
- ⚡ Powered by Google Gemini API via the `llm` CLI tool

![Screenshot](https://github.com/johndoe422/ezbash/raw/main/screenshots/Screenshot%202025-11-04%20234129.png)

## Prerequisites

- Python 3.6 or higher
- A Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))
- Linux/Unix-based system with bash

## Installation

### 1. Create and Activate Virtual Environment

```bash
# Create the project directory
mkdir ezbash
cd ezbash

# Create virtual environment
python3 -m venv ezbashenv

# Activate the environment
source ezbashenv/bin/activate
```

Your prompt should now start with `(ezbashenv)`.

### 2. Install Dependencies

```bash
# Install the llm CLI tool
pip install llm

# Install the Gemini plugin
llm install llm-gemini
```

### 3. Configure API Key

```bash
# Set your Gemini API key
llm keys set gemini
```

When prompted, paste your API key.

### 4. Set Default Model

```bash
# Use the efficient Gemini Flash model as default
llm models default gemini-2.5-flash
```

### 5. Download the Script

Download `ezbash.py` from this repository and place it in your `ezbash` folder.

### 6. Create the Shell Wrapper

Edit your bash configuration:

```bash
nano ~/.bashrc
```

Add this function at the end of the file. **Update the paths** to match your system:

```bash
# ezbash - Natural language command generator
run() {
  # Activate the virtual environment silently
  source /path/to/ezbash/ezbashenv/bin/activate > /dev/null 2>&1
  
  # Call the Python script with all arguments
  python /path/to/ezbash/ezbash.py "$@"
  
  # Deactivate the virtual environment
  deactivate
}
```

Replace `/path/to/ezbash` with your actual path (e.g., `/home/username/ezbash`).

### 7. Apply Changes

```bash
source ~/.bashrc
```

## Usage

Simply use the `run` command followed by your task in natural language:

```bash
run 'find files larger than 50MB in the home directory'
run 'show disk usage sorted by size'
run 'enable ipv4 and ipv6 forwarding and persist the changes'
run 'list all processes using port 8080'
```

### Interactive Options

After a command is generated, you'll see:

```
✅ Generated Command:
   find ~ -type f -size +50M

Execute? (Y/n):
```

- **Y** or **Enter**: Execute the command immediately
- **n**: Cancel without executing

## How It Works

1. You describe what you want in natural language
2. ezbash sends your request to the Gemini LLM via the `llm` CLI tool
3. The generated command is displayed for review
4. You decide whether to execute or cancel
5. Only approved commands are executed

## Safety Notes

- **Always review** generated commands before executing
- Commands with `sudo` or destructive operations require extra caution
- Use the clipboard option (c) to manually edit commands before running
- The LLM may occasionally generate incorrect commands - human review is essential

## Troubleshooting

### Command not found: run

Make sure you've sourced your `.bashrc`:
```bash
source ~/.bashrc
```

### Virtual environment issues

Verify the paths in your `run` function match your actual installation directory.

### API errors

Ensure your Gemini API key is set correctly:
```bash
llm keys set gemini
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with [llm](https://github.com/simonw/llm) by Simon Willison
- Powered by Google Gemini API
