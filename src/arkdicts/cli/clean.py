import os
import click
import shutil
from pathlib import Path
from typing import List
from arkdicts.constant import PRESERVED_PATHS, OUTPUT_DIR


@click.command("clean")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--quiet", "-q", is_flag=True, help="Enable quiet output")
def command(
    work_directory: str = OUTPUT_DIR,
    preserved_paths: List[str] = PRESERVED_PATHS,
    quiet: bool = False,
    verbose: bool = False,
) -> None:
    work_dir = Path(work_directory).resolve()

    if not work_dir.exists():
        click.echo(
            click.style(
                f"The working directory does not exist: {work_directory}", fg="red"
            ),
            err=True,
        )
        raise click.Abort()

    if not work_dir.is_dir():
        click.echo(
            click.style(
                f"The working directory is not a folder: {work_directory}", fg="red"
            ),
            err=True,
        )
        raise click.Abort()

    preserved_abs_paths = set()
    for rel_path in preserved_paths:
        abs_path = (work_dir / rel_path).resolve()

        try:
            abs_path.relative_to(work_dir)
        except ValueError:
            click.echo(
                click.style(
                    f"Preserve paths outside the working directory range: {rel_path}",
                    fg="red",
                ),
                err=True,
            )
            raise click.Abort()
        preserved_abs_paths.add(abs_path)

    all_preserved_paths = set(preserved_abs_paths)

    for path in preserved_abs_paths:
        current = path
        while current != work_dir and current.parent != current:
            all_preserved_paths.add(current.parent)
            current = current.parent

    def should_delete(path: Path) -> bool:
        return path not in all_preserved_paths

    def safe_delete(path: Path) -> None:
        try:
            if path.is_file() or path.is_symlink():
                path.unlink()
                if verbose and not quiet:
                    click.echo(f"Deleted file: {path.relative_to(work_dir)}")
            elif path.is_dir():
                shutil.rmtree(path)
                if verbose and not quiet:
                    click.echo(f"Deleted folder: {path.relative_to(work_dir)}")
        except Exception as e:
            click.echo(
                click.style(
                    f"Failed to delete {path.relative_to(work_dir)}: {e}", fg="red"
                ),
                err=True,
            )

    items_to_process = []
    for root, dirs, files in os.walk(work_dir, topdown=False):
        root_path = Path(root)

        for file in files:
            file_path = root_path / file
            items_to_process.append(file_path)

        for dir_name in dirs:
            dir_path = root_path / dir_name
            items_to_process.append(dir_path)

    items_to_process.sort(key=lambda x: len(str(x)), reverse=True)

    deleted_count = 0
    error_count = 0

    for item_path in items_to_process:
        if should_delete(item_path):
            deleted_count += 1
            safe_delete(item_path)

    if not quiet:
        if verbose:
            click.echo(f"\nCleanup complete: {deleted_count} items deleted")
            if error_count > 0:
                click.echo(f"Deletion of {error_count} items failed", err=True)
        else:
            click.echo(f"Cleanup complete: {deleted_count} items deleted")
