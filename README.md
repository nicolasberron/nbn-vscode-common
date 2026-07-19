# nbn-vscode-common

Shared VS Code tasks and GitHub Copilot skills for use across repositories.

## Contents

- `.vscode/tasks.json` contains the common tasks shipped with this repository.
- `.github/skills/` contains Copilot Agent Skills. Skills are kept in the repository so they can be versioned and updated together.
- `scripts/install-global.py` installs both into the current user's global configuration.

## Install globally from this repository

From the repository root, run:

```sh
python scripts/install-global.py
```

This installs:

1. The repository tasks as VS Code user tasks in `~/.config/Code/User/tasks.json`, so they are available in every workspace.
2. Each skill under `.github/skills/` in `~/.copilot/skills/`. Symbolic links are used by default, so pulling repository updates makes the global skills immediately available.

An existing VS Code user task file is backed up beside itself before installation. Reload VS Code after installation if the tasks or skills do not appear immediately.

### Installation options

Show all options:

```sh
python scripts/install-global.py --help
```

Useful examples:

```sh
# Copy skills instead of linking them to this checkout
python scripts/install-global.py --copy-skills

# Use a non-default VS Code user directory
python scripts/install-global.py --vscode-user-dir "$HOME/.config/Code - Insiders/User"

# Use a different global Copilot skills directory
python scripts/install-global.py --skills-dir "$HOME/.copilot/skills"
```

The paths can also be set with `VSCODE_USER_DIR` and `COPILOT_SKILLS_DIR` environment variables. The installer is safe to run again after updating this repository; it replaces the installed task and skill definitions and creates a new backup for an existing task file.

## Use in this repository only

The tasks are also available directly from this repository through **Terminal → Run Task**. Copilot recognizes skills in `.github/skills/` when this repository is open, without a global installation.

## Updating or removing the global installation

To update the global installation, pull the latest repository changes and run the installer again. To remove the installed skills, delete the links or copied directories under `~/.copilot/skills/`. To remove the installed tasks, restore the most recent `tasks.json.nbn-vscode-common.*.bak` file or delete `~/.config/Code/User/tasks.json` if it did not contain other user tasks.

The installer does not modify repository files and does not run project builds or tests.
