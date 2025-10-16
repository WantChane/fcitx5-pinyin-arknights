import click
from arkdicts.constant import ALL_DICTS


@click.command(name="list")
def command():
    click.echo("Available dictionaries:")
    for i, name in enumerate(sorted(ALL_DICTS), 1):
        click.echo(f"{i:>2}. {name}")
