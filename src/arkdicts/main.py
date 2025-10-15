import click
from arkdicts.cli import diff, stat, update, list, clean, build, label


@click.group()
def main() -> None:
    pass


main.add_command(diff.command)
main.add_command(stat.command)
main.add_command(update.command)
main.add_command(list.command)
main.add_command(clean.command)
main.add_command(build.command)
main.add_command(label.command)

if __name__ == "__main__":
    main()
