# Agtx

## The simplest ever coding agent. Fully local, simple operations, unlimited possibilities.


Agtx is a simple and clear coding assistant that lives directly in your terminal. Instead of using complex software layers or heavy setups, Agtx uses a straightforward loop to read your local files, make precise edits, run tests, and save stable git checkpoints.

It is completely open, transparent, and gives you full control over your code.

### Development Status: Active Work in Progress

Please note: Agtx is currently being built and is not ready for everyday production use. Features are still being created, tested, and changed. Things might break often as we work on the core code.

### Key Features

Fully Local: Agtx runs completely on your own computer. It only works inside the folder you choose, keeping your files safe and private.

Smart Line Editing: Instead of rewriting whole files, Agtx finds the exact lines of code that need to change and swaps them out quickly.

Bring Your Own Key (BYOK): Connect easily to OpenRouter. It takes seconds to set up and saves your API key securely in your local settings.

Safety First: Safe operations are built-in. If the agent tries to run a risky command, it pauses and waits for you to type "y" to approve it.

Git Checkpoints: Agtx checks your repository status, tests the changes, and saves git commits automatically when things work. If a test fails, it can undo the changes.

### Installation

To install Agtx globally in editable mode, clone the repository and run the setup:
```
git clone [https://github.com/aaravriyer193/Agtx-code.git](https://github.com/aaravriyer193/Agtx-code.git)
cd Agtx-code
pip install -e .
```

Installing with the -e flag links the terminal command directly to your folder. Any changes made to the Python files will update your terminal tool instantly.

### Quick Start

Go to any project folder on your computer and start the agent:

```
agtx
```

On your first run, Agtx will ask you for:

Your OpenRouter API key (saved locally in settings.json).

Your working directory (you can use your current folder).

The model you want to use (like xiaomi/mimo-v2.5-pro).

Once set up, type your request:

You: convert the basic calculator component to a graphing calculator using chart.js


### File Architecture

The project files are simple and easy to customize:

```

main.py - The main loop that runs the agent and directs tools.

Utils/apicall.py - The simple script to send requests to OpenRouter.

Utils/prompts.py - The instructions that guide the agent.

Tools/createfile.py - Tool to write new files.

Tools/readfile.py - Tool to open and read files.

Tools/replaceinfile.py - Tool to find and change specific lines of code.

Tools/presentfiles.py - Tool to map your project folder tree.

Tools/execute.py - Tool to run terminal commands safely.

Tools/gitmanager.py - Tool to handle git saves and resets.

```

### Configuration

Your local preferences are saved in settings.json. This file is ignored by Git automatically so your private keys never get uploaded online.
```
{
    "openrouter_api_key": "your-key-here",
    "working_directory": "/path/to/project",
    "model": "xiaomi/mimo-v2.5-pro",
    "terminal_timeout": 30
}
```

### License

This project is licensed under the MIT License.
