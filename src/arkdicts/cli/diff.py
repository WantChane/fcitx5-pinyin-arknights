import re
from typing import List
import click
import os
from dataclasses import dataclass, field
from pathlib import Path
from arkdicts.utils.utils import echo_or_github_output


@dataclass
class MarkdownContent:
    lines: List[str] | None = None

    def append(self, text: str, echo: bool = False, **kwargs):
        if self.lines is not None and len(self.lines) >= 0:
            self.lines.append(text)
        if echo or kwargs:
            click.echo(click.style(text, **kwargs), nl=False)

    def pop(self):
        return (
            self.lines.pop() if self.lines is not None and len(self.lines) > 0 else None
        )

    def peek(self):
        return (
            self.lines[-1] if self.lines is not None and len(self.lines) > 0 else None
        )

    def save(self, path: Path):
        if self.lines is not None and len(self.lines) >= 0:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(self.lines)


@dataclass
class DiffProcessor:
    markdown_content: MarkdownContent = field(default_factory=MarkdownContent)
    ignore_content_regex: re.Pattern = re.compile(r"^version: ")
    ignore_extensions: List[str] = field(default_factory=lambda: [".md", ".dict"])

    def content_to_set(self, filename: str):
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

    def files_to_set(self, directory: str):
        directory_path = Path(directory)
        files = [
            str(file_path.relative_to(directory_path))
            for file_path in directory_path.rglob("*")
            if file_path.is_file()
            and file_path.suffix.lower() not in self.ignore_extensions
        ]
        return set(files)

    def diff_file(self, file1, file2, verbose=False):
        if file1 is None and file2 is None:
            return False
        set1 = self.content_to_set(file1) if file1 else set()
        set2 = self.content_to_set(file2) if file2 else set()

        if not verbose and set1 == set2:
            return False

        only_in_file1 = sorted(set1 - set2)
        only_in_file2 = sorted(set2 - set1)

        self.markdown_content.append("```diff\n")
        if not only_in_file1:
            self.markdown_content.append(f"+++ new: {file2}\n", fg="green")
        elif not only_in_file2:
            self.markdown_content.append(f"--- old: {file1}\n", fg="red")
        else:
            self.markdown_content.append(f"--- old: {file1}\n", fg="red")
            self.markdown_content.append(f"+++ new: {file2}\n", fg="green")

        self.markdown_content.append(
            f"@@ -{len(only_in_file1)},{len(set2)} +{len(only_in_file2)},{len(set2)} @@\n",
            fg="cyan",
        )
        for line in only_in_file1:
            self.markdown_content.append(f"- {line}\n", fg="red", bold=True)
        for line in only_in_file2:
            self.markdown_content.append(f"+ {line}\n", fg="green", bold=True)

        self.markdown_content.append("```\n")

        return set1 != set2

    def diff_directory(self, dir1, dir2):
        files1 = self.files_to_set(dir1)
        files2 = self.files_to_set(dir2)

        all_files = sorted(files1 | files2, key=lambda x: Path(x).name)

        result = False

        for relative_file in all_files:
            header_line = f"# {relative_file}\n\n"
            self.markdown_content.append(header_line)
            file1_path = Path(dir1) / relative_file
            file2_path = Path(dir2) / relative_file
            diff_result = False
            if relative_file in files1 and relative_file in files2:
                diff_result = self.diff_file(
                    str(file1_path), str(file2_path), verbose=False
                )

            elif relative_file in files1:
                diff_result = self.diff_file(str(file1_path), None)

            elif relative_file in files2:
                diff_result = self.diff_file(None, str(file2_path))

            if not diff_result:
                self.markdown_content.pop()
            else:
                self.markdown_content.append("\n", echo=True)
            result |= diff_result
        return result


@click.command(name="diff")
@click.argument("path1", type=click.Path(exists=True), required=True)
@click.argument("path2", type=click.Path(exists=True), required=True)
@click.option("-m", "--markdown", type=click.Path(), default=None)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
)
def command(path1, path2, markdown, verbose):
    markdown_content = MarkdownContent(lines=[]) if markdown else MarkdownContent()
    diff_processor = DiffProcessor(markdown_content)
    result = False

    if os.path.isfile(path1) and os.path.isfile(path2):
        result |= diff_processor.diff_file(path1, path2, verbose)

    elif os.path.isdir(path1) and os.path.isdir(path2):
        result |= diff_processor.diff_directory(path1, path2)

    else:
        click.echo(
            click.style("Error: Cannot compare a directory with a file.", fg="red")
        )
    echo_or_github_output({"diff_result": str(result).lower()}, verbose)
    markdown_content.save(markdown)
