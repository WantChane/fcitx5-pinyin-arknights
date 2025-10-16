import os
from typing import Optional
import click
import requests
from arkdicts.constant import ROOT_DIR
from arkdicts.cli import build
from arkdicts.utils.utils import echo_or_github_output


def get_raw_github_file(
    owner: str, repo: str, path: str, branch: str = "main"
) -> Optional[str]:
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

    try:
        response = requests.get(raw_url, timeout=10)
        response.raise_for_status()
        return response.content.decode("utf-8").strip()
    except requests.exceptions.RequestException as e:
        click.echo(
            click.style(f"Failed to get {owner}/{repo}/{path}: {e}", fg="red"), err=True
        )
        return None


def read_local_version(version_file: str) -> Optional[str]:
    if not os.path.exists(version_file):
        return None
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    except IOError as e:
        click.echo(
            click.style(f"Failed to read the verison file: {e}", fg="red"), err=True
        )
        return None


def write_local_version(version_file: str, version: str) -> bool:
    try:
        with open(version_file, "w", encoding="utf-8") as f:
            f.write(version)
        return True
    except IOError as e:
        click.echo(
            click.style(f"Failed to write the version file: {e}", fg="red"), err=True
        )
        return False


def check_version(version_file):
    current_version = get_raw_github_file(
        "yuanyan3060", "ArknightsGameResource", "version"
    )

    old_version = read_local_version(version_file)
    version_changed = current_version != old_version

    output_data = {
        "version_changed": str(version_changed).lower(),
        "current_version": current_version,
    }

    echo_or_github_output(output_data)

    if version_changed and current_version:
        write_local_version(version_file, current_version)
        click.echo(f"Version updated: {current_version}")
    else:
        click.echo(f"Version unchanged: {current_version}")

    return version_changed


@click.command(name="update")
@click.option(
    "-s",
    "--select",
    "select_dictionaries",
    multiple=True,
    envvar="AD_UPDATE_SELECT_DICTIONARIES",
)
@click.pass_context
def command(ctx, select_dictionaries):
    if check_version(ROOT_DIR / "version"):
        click.echo("New version detected, rebuilding dictionaries...")
        ctx.invoke(
            build.command,
            all_flag=True,
        )
    elif select_dictionaries:
        click.echo(
            "No new version detected, but --select specified, rebuilding selected dictionaries..."
        )
        ctx.invoke(
            build.command,
            select_dictionaries=select_dictionaries,
        )
    else:
        click.echo("No new version detected, skipping rebuild.")
