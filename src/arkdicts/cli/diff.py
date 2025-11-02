import re
from typing import List, Iterator, Optional, Tuple
import click
import os
from dataclasses import dataclass, field
from pathlib import Path
from arkdicts.utils.utils import echo_or_github_output
import contextlib
import tempfile
import shutil
import subprocess
import tarfile
import io


@contextlib.contextmanager
def git_ref_path(resource: str) -> Iterator[Tuple[str, str]]:
    if ":" not in resource:
        if not os.path.exists(resource):
            raise click.ClickException(f"Path '{resource}' does not exist")
        try:
            yield (resource, resource)
        finally:
            pass
        return

    ref, git_path = resource.split(":", 1)
    display_path = f"{ref}:{git_path}"
    temp_dir = tempfile.mkdtemp()

    try:
        archive_command = ["git", "archive", "--format=tar", ref, git_path]
        result = subprocess.run(
            archive_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r") as tar:
            tar.extractall(path=temp_dir)

        extracted_path = os.path.join(temp_dir, git_path)
        if not os.path.exists(extracted_path):
            raise click.ClickException(
                f"Path '{git_path}' does not exist in ref '{ref}' after extraction"
            )

        yield (display_path, extracted_path)

    except subprocess.CalledProcessError as e:
        raise click.ClickException(
            f"Failed to extract '{resource}': {e.stderr.decode().strip()}"
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@dataclass
class MarkdownContent:
    lines: List[str] | None = None

    def append(self, text: str, echo: bool = False, **kwargs) -> None:
        if self.lines is not None and len(self.lines) >= 0:
            self.lines.append(text)
        if echo or kwargs:
            click.echo(click.style(text, **kwargs), nl=False)

    def pop(self) -> str | None:
        return self.lines.pop() if self.lines is not None and self.lines else None

    def peek(self) -> str | None:
        return self.lines[-1] if self.lines is not None and self.lines else None

    def save(self, path: str | Path) -> None:
        if self.lines is not None and self.lines:
            path = Path(path)
            with path.open("w", encoding="utf-8") as f:
                f.writelines(self.lines)


@dataclass
class DiffProcessor:
    markdown_content: MarkdownContent = field(default_factory=MarkdownContent)
    ignore_content_regex: re.Pattern = re.compile(r"^version: ")
    ignore_extensions: List[str] = field(default_factory=lambda: [".md", ".dict"])

    path_mapping: dict = field(default_factory=dict)

    def format_path(self, path: str) -> str:
        return self.path_mapping.get(
            path, Path(path).name if os.path.isfile(path) else path
        )

    def content_to_set(self, filename: str) -> set:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = (
                    line.rstrip("\n")
                    for line in f
                    if not self.ignore_content_regex.search(line) and line.strip() != ""
                )
                return set(lines)
        except FileNotFoundError:
            return set()
        except UnicodeDecodeError:
            return set()

    def files_to_set(self, directory: str) -> set:
        directory_path = Path(directory)
        files = [
            str(file_path.relative_to(directory_path))
            for file_path in directory_path.rglob("*")
            if file_path.is_file()
            and file_path.suffix.lower() not in self.ignore_extensions
        ]
        return set(files)

    def diff_file(
        self,
        file1: Optional[str],
        file2: Optional[str],
        file1_display: Optional[str],
        file2_display: Optional[str],
        verbose: bool = False,
    ) -> bool:
        set1 = self.content_to_set(file1) if file1 and os.path.exists(file1) else set()
        set2 = self.content_to_set(file2) if file2 and os.path.exists(file2) else set()

        if not verbose and set1 == set2:
            return False

        only_in_file1 = sorted(set1 - set2)
        only_in_file2 = sorted(set2 - set1)

        self.markdown_content.append("```diff\n")
        self.markdown_content.append(f"--- {file1_display}\n", fg="red")
        self.markdown_content.append(f"+++ {file2_display}\n", fg="green")

        self.markdown_content.append(
            f"@@ -{len(only_in_file1)},{len(set1)} +{len(only_in_file2)},{len(set2)} @@\n",
            fg="cyan",
        )
        for line in only_in_file1:
            self.markdown_content.append(f"- {line}\n", fg="red", bold=True)
        for line in only_in_file2:
            self.markdown_content.append(f"+ {line}\n", fg="green", bold=True)

        self.markdown_content.append("```\n")

        return set1 != set2

    def diff_directory(
        self, dir1: str, dir2: str, dir1_display: str, dir2_display: str
    ) -> bool:
        files1 = self.files_to_set(dir1) if os.path.isdir(dir1) else set()
        files2 = self.files_to_set(dir2) if os.path.isdir(dir2) else set()

        all_files = sorted(files1 | files2, key=lambda x: Path(x).name)

        if not all_files:
            self.markdown_content.append(
                f"# Both directories are empty: {dir1_display}\n\n"
            )
            return False

        result = False

        for relative_file in all_files:
            header_line = f"# {relative_file}\n\n"
            self.markdown_content.append(header_line)
            file1_path = Path(dir1) / relative_file
            file2_path = Path(dir2) / relative_file

            file1_display = f"{dir1_display}/{relative_file}"
            file2_display = f"{dir2_display}/{relative_file}"

            diff_result = False
            if relative_file in files1 and relative_file in files2:
                diff_result = self.diff_file(
                    str(file1_path),
                    str(file2_path),
                    file1_display,
                    file2_display,
                    verbose=False,
                )
            elif relative_file in files1:
                diff_result = self.diff_file(
                    str(file1_path), None, file1_display, "DELETED", verbose=False
                )
            elif relative_file in files2:
                diff_result = self.diff_file(
                    None, str(file2_path), "ADDED", file2_display, verbose=False
                )

            if not diff_result:
                self.markdown_content.pop()
            else:
                self.markdown_content.append("\n", echo=True)

            result |= diff_result
        return result


@click.command(name="diff")
@click.argument("path1", type=click.Path(), required=True)
@click.argument("path2", type=click.Path(), required=True)
@click.option("-m", "--markdown", type=click.Path(), default=None)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
)
def command(path1: str, path2: str, markdown: str | None, verbose: bool):
    with (
        git_ref_path(path1) as (display1, real1),
        git_ref_path(path2) as (display2, real2),
    ):
        markdown_content = MarkdownContent(lines=[]) if markdown else MarkdownContent()
        diff_processor = DiffProcessor(markdown_content)

        diff_processor.path_mapping = {real1: display1, real2: display2}

        result = False
        is_file1 = os.path.isfile(real1)
        is_file2 = os.path.isfile(real2)
        is_dir1 = os.path.isdir(real1)
        is_dir2 = os.path.isdir(real2)

        if is_file1 and is_file2:
            result = diff_processor.diff_file(real1, real2, display1, display2, verbose)

        elif is_dir1 and is_dir2:
            result = diff_processor.diff_directory(real1, real2, display1, display2)

        else:
            click.echo(
                click.style("Error: Cannot compare directory with file", fg="red")
            )

        echo_or_github_output({"diff_result": str(result).lower()}, verbose)

        if markdown:
            diff_processor.markdown_content.save(markdown)
