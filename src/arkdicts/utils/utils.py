import click
import os
from arkdicts.constant import OUTPUT_DIR


def generate_filepath(dict_name: str) -> tuple[str, str, str]:
    titles_path = f"{OUTPUT_DIR}/titles/{dict_name}_titles.txt"
    rime_path = f"{OUTPUT_DIR}/rime_dicts/{dict_name}.dict.yaml"
    fcitx_path = f"{OUTPUT_DIR}/fcitx5_dicts/{dict_name}.dict"
    return titles_path, rime_path, fcitx_path


def echo_or_github_output(message: dict, verbose: bool = False):
    if "GITHUB_OUTPUT" in os.environ:
        try:
            with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
                for key, value in message.items():
                    fh.write(f"{key}={value}\n")
        except IOError as e:
            click.echo(
                click.style(
                    f"Failed to write {os.environ['GITHUB_OUTPUT']}: {e}", fg="red"
                ),
                err=True,
            )
    elif verbose:
        for key, value in message.items():
            click.echo(f"{key}={value}")
