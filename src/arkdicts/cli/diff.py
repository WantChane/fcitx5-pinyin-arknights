import click


def read_file_to_set(filename):
    with open(filename, "r") as f:
        return {line.rstrip("\n") for line in f}


def diff_file(file1, file2):
    set1 = read_file_to_set(file1)
    set2 = read_file_to_set(file2)

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
        click.echo(click.style(f"-{line}", fg="red", bold=True))

    for line in only_in_file2:
        click.echo(click.style(f"+{line}", fg="green", bold=True))


@click.command(name="diff")
@click.argument("path1", type=click.Path(exists=True), required=True)
@click.argument("path2", type=click.Path(exists=True), required=True)
def command(path1, path2):
    diff_file(path1, path2)
