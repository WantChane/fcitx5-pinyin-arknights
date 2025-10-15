import re
import click
import os
from pathlib import Path


def regex_filter(pattern):
    compiled_pattern = re.compile(pattern)
    return lambda line: not bool(compiled_pattern.search(line))


def read_file_to_set(filename, filter=regex_filter(r"^version: ")):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            if filter is not None:
                lines = (line.rstrip("\n") for line in f if filter(line))
            else:
                lines = (line.rstrip("\n") for line in f)
            return set(lines)

    except FileNotFoundError:
        return set()
    except UnicodeDecodeError:
        return set()


def diff_file(file1, file2, quiet=False):
    set1 = read_file_to_set(file1)
    set2 = read_file_to_set(file2)

    if quiet and set1 == set2:
        return False

    only_in_file1 = sorted(set1 - set2)
    only_in_file2 = sorted(set2 - set1)

    click.echo(click.style(f"--- old: {file1}", fg="red"))
    click.echo(click.style(f"+++ new: {file2}", fg="green"))

    click.echo(
        click.style(
            f"@@ -{len(only_in_file1)},{len(set1)} +{len(only_in_file2)},{len(set2)} @@",
            fg="cyan",
        )
    )

    for line in only_in_file1:
        click.echo(click.style(f"- {line}", fg="red", bold=True))

    for line in only_in_file2:
        click.echo(click.style(f"+ {line}", fg="green", bold=True))
    click.echo()

    return True


def get_relative_files(directory):
    relative_files = []
    directory_path = Path(directory)
    ignored_extensions = {".dict", ".diff"}

    relative_files = [
        str(file_path.relative_to(directory_path))
        for file_path in directory_path.rglob("*")
        if file_path.is_file() and file_path.suffix.lower() not in ignored_extensions
    ]

    return set(relative_files)


def diff_directory(dir1, dir2):
    files1 = get_relative_files(dir1)
    files2 = get_relative_files(dir2)

    all_files = sorted(files1 | files2, key=lambda x: Path(x).name)

    for relative_file in all_files:
        file1_path = Path(dir1) / relative_file
        file2_path = Path(dir2) / relative_file

        if relative_file in files1 and relative_file in files2:
            diff_file(str(file1_path), str(file2_path), quiet=True)

        elif relative_file in files1:
            diff_file_with_empty(str(file1_path), side="new")

        elif relative_file in files2:
            diff_file_with_empty(str(file2_path), side="old")


def diff_file_with_empty(file_path, side="both"):
    set1 = set()
    set2 = set()
    if side == "old":
        set1 = read_file_to_set(file_path)
        click.echo(click.style(f"--- old: {file_path}", fg="red"))
        click.echo(
            click.style(
                f"@@ -{len(set1)} @@",
                fg="cyan",
            )
        )
        for line in set1:
            click.echo(click.style(f"- {line}", fg="red", bold=True))
        click.echo()

    elif side == "new":
        set2 = read_file_to_set(file_path)
        click.echo(click.style(f"+++ new: {file_path}", fg="green"))
        click.echo(
            click.style(
                f"@@ +{len(set2)} @@",
                fg="cyan",
            )
        )
        for line in set2:
            click.echo(click.style(f"+ {line}", fg="green", bold=True))
        click.echo()

    else:
        click.echo(click.style("Error: side must be 'old' or 'new'.", fg="red"))
        raise click.Abort()


@click.command(name="diff")
@click.argument("path1", type=click.Path(exists=True), required=True)
@click.argument("path2", type=click.Path(exists=True), required=True)
def command(path1, path2):
    if os.path.isfile(path1) and os.path.isfile(path2):
        diff_file(path1, path2)

    elif os.path.isdir(path1) and os.path.isdir(path2):
        diff_directory(path1, path2)

    else:
        click.echo(
            click.style("Error: Cannot compare a directory with a file.", fg="red")
        )
