import os
from typing import Optional
import click
import requests


def get_raw_github_file(
    owner: str, repo: str, path: str, branch: str = "main"
) -> Optional[str]:
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

    try:
        response = requests.get(raw_url, timeout=10)
        response.raise_for_status()
        return response.content.decode("utf-8").strip()
    except requests.exceptions.RequestException as e:
        click.echo(f"Failed to get {owner}/{repo}/{path}: {e}", err=True)
        return None


def read_local_version(version_file: str) -> Optional[str]:
    if not os.path.exists(version_file):
        return None
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    except IOError as e:
        click.echo(f"Failed to read the verison file: {e}", err=True)
        return None


def write_local_version(version_file: str, version: str) -> bool:
    try:
        with open(version_file, "w", encoding="utf-8") as f:
            f.write(version)
        return True
    except IOError as e:
        click.echo(f"Failed to write the version file: {e}", err=True)
        return False


@click.command(name="update")
def command():
    VERSION_FILE = "version"

    current_version = get_raw_github_file(
        "yuanyan3060", "ArknightsGameResource", "version"
    )

    old_version = read_local_version(VERSION_FILE)
    version_changed = current_version != old_version

    output_data = {
        "changed": str(version_changed).lower(),
        "current_version": current_version,
    }

    if "GITHUB_OUTPUT" in os.environ:
        try:
            with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
                for key, value in output_data.items():
                    fh.write(f"{key}={value}\n")
        except IOError as e:
            click.echo(f"Failed to write {os.environ['GITHUB_OUTPUT']}: {e}", err=True)
    else:
        for key, value in output_data.items():
            click.echo(f"{key}={value}")

    if version_changed and current_version:
        write_local_version(VERSION_FILE, current_version)
        click.echo(f"Version updated: {current_version}")
    else:
        click.echo(f"Version unchanged: {current_version}")


if __name__ == "__main__":
    command()

