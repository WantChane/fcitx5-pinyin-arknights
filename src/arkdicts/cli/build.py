import click
from arkdicts.constant import ALL_DICTS
from mw2fcitx.main import inner_main


def build_dictionary(dict_name):
    if dict_name in ALL_DICTS:
        try:
            inner_main(["-c", f"./src/arkdicts/conf/{dict_name}.py"])
            click.echo(f"Successfully built {dict_name}")
        except Exception as e:
            click.echo(f"Failed to build {dict_name}: {e}", err=True)


@click.command(name="build")
@click.option(
    "-a",
    "--all",
    "all_flag",
    is_flag=True,
    default=False,
    help="选择所有",
)
@click.option(
    "-s",
    "--select",
    "select_values",
    multiple=True,
    help="多选项目",
)
def command(all_flag, select_values):
    if not all_flag and not select_values:
        click.echo(
            "Warning: No --select or --all specified, defaulting to --all", err=True
        )
        all_flag = True

    if all_flag and select_values:
        click.echo(
            "Warning: --select and --all exist at the same time, --select takes precedence",
            err=True,
        )
        all_flag = False

    selected_set = set()
    if all_flag:
        selected_set = ALL_DICTS
    elif select_values:
        selected_set = set(select_values)
        if not selected_set.issubset(ALL_DICTS):
            invalid_selections = selected_set - ALL_DICTS
            click.echo(
                f"Error: The following dictionaies are invalid: {', '.join(invalid_selections)}",
                err=True,
            )
            click.echo(f"Available dictionaries: {', '.join(sorted(ALL_DICTS))}")
            raise click.Abort()

    for d in selected_set:
        build_dictionary(d)
