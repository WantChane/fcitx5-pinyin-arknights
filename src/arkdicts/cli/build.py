import click
from arkdicts.constant import ALL_DICTS, CONF_DIR
from mw2fcitx.main import inner_main


def build_dictionary(dict_name):
    if dict_name in ALL_DICTS:
        try:
            inner_main(["-c", f"{CONF_DIR}/{dict_name}.py"])
            click.echo(click.style(f"Successfully built {dict_name}", fg="green"))
        except Exception as e:
            click.echo(
                click.style(f"Failed to build {dict_name}: {e}", fg="red"), err=True
            )


@click.command(name="build")
@click.option(
    "-a",
    "--all",
    "all_flag",
    is_flag=True,
    default=False,
)
@click.option(
    "-s",
    "--select",
    "select_values",
    multiple=True,
)
def command(all_flag, select_values):
    if not all_flag and not select_values:
        click.echo(
            click.style(
                "Warning: No --select or --all specified, defaulting to --all", fg="red"
            ),
            err=True,
        )
        all_flag = True

    if all_flag and select_values:
        click.echo(
            click.style(
                "Warning: --select and --all exist at the same time, --select takes precedence",
                fg="red",
            ),
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
                click.style(
                    f"Error: The following dictionaies are invalid: {', '.join(invalid_selections)}",
                    fg="red",
                ),
                err=True,
            )
            click.echo(
                click.style(
                    f"Available dictionaries: {', '.join(sorted(ALL_DICTS))}", fg="red"
                )
            )
            raise click.Abort()

    for d in selected_set:
        build_dictionary(d)
