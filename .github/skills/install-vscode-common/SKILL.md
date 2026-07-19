---
name: install-vscode-common
description: Install or update the shared VS Code tasks and Copilot skills from nbn-vscode-common for use across repositories. Use when setting up global VS Code tasks, installing shared Copilot skills, or updating this common configuration.
---

# Install VS Code common configuration

Run the repository installer from the root of this repository:

```sh
python scripts/install-global.py
```

The installer:

- backs up an existing VS Code user task file before replacing it;
- installs the tasks in `.vscode/tasks.json` as user tasks, making them available in every workspace;
- links every skill under `.github/skills/` into `~/.copilot/skills/`;
- can be run again after pulling changes to update the global installation.

Use `python scripts/install-global.py --help` for options, including a custom VS Code user directory and copy mode instead of symbolic links. Restart or reload VS Code after installing so the task list is refreshed. On systems where the executable is named `python3`, use that name instead.
