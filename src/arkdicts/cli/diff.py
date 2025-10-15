import click


def read_file_to_set(filename):
    with open(filename, "r") as f:
        return {line.rstrip("\n") for line in f}


@click.command(name="diff")
@click.argument("file1", type=click.Path(exists=True), required=True)
@click.argument("file2", type=click.Path(exists=True), required=True)
def command(file1, file2):
    set1 = read_file_to_set(file1)
    set2 = read_file_to_set(file2)

    only_in_file1 = sorted(set1 - set2)
    only_in_file2 = sorted(set2 - set1)

    click.echo(f"--- {file1}")
    click.echo(f"+++ {file2}")

    for line in only_in_file1:
        click.echo(f"< {line}")

    if only_in_file1 and only_in_file2:
        click.echo("---")

    for line in only_in_file2:
        click.echo(f"> {line}")
