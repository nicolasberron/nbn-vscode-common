#!/usr/bin/env python3
"""Install the repository's VS Code tasks and Copilot skills globally."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def default_vscode_user_dir() -> Path:
    """Return the default VS Code User directory for the current platform."""
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Code" / "User"
    if os.name == "nt":
        app_data = os.environ.get("APPDATA")
        if app_data:
            return Path(app_data) / "Code" / "User"
        return Path.home() / "AppData" / "Roaming" / "Code" / "User"
    config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
    return Path(config_home) / "Code" / "User"


def remove_path(path: Path) -> None:
    """Remove a file, symlink, or directory without following symlinks."""
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def install_skill(source: Path, target: Path, copy_skills: bool) -> None:
    if target.exists() or target.is_symlink():
        remove_path(target)
    if copy_skills:
        shutil.copytree(source, target)
        return
    try:
        target.symlink_to(source, target_is_directory=True)
    except (OSError, NotImplementedError):
        print(
            f"Could not create a symbolic link for {source.name}; copying instead."
        )
        shutil.copytree(source, target)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install nbn-vscode-common tasks and Copilot skills globally."
    )
    parser.add_argument(
        "--copy-skills",
        action="store_true",
        help="copy skills instead of creating symbolic links",
    )
    parser.add_argument(
        "--vscode-user-dir",
        type=Path,
        default=Path(os.environ.get("VSCODE_USER_DIR", default_vscode_user_dir())),
        help="VS Code User directory",
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=Path(
            os.environ.get("COPILOT_SKILLS_DIR", Path.home() / ".copilot" / "skills")
        ),
        help="global Copilot skills directory",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    tasks_source = repo_root / ".vscode" / "tasks.json"
    skills_source = repo_root / ".github" / "skills"
    tasks_target = args.vscode_user_dir / "tasks.json"

    args.vscode_user_dir.mkdir(parents=True, exist_ok=True)
    args.skills_dir.mkdir(parents=True, exist_ok=True)

    if tasks_target.exists() or tasks_target.is_symlink():
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup = tasks_target.with_name(
            f"{tasks_target.name}.nbn-vscode-common.{timestamp}.bak"
        )
        shutil.copy2(tasks_target, backup)
        print(f"Backed up existing user tasks to {backup}")

    shutil.copy2(tasks_source, tasks_target)
    print(f"Installed VS Code user tasks at {tasks_target}")

    for skill_source in sorted(path for path in skills_source.iterdir() if path.is_dir()):
        install_skill(skill_source, args.skills_dir / skill_source.name, args.copy_skills)
        print(f"Installed Copilot skill: {skill_source.name}")

    print("Global installation complete. Reload VS Code to refresh tasks and Copilot skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())