import click
import os
from arkdicts.constant import OUTPUT_DIR
from arkdicts.constant import (
    BUILD_DATE,
    FIXFILE_FILE,
)


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


def generate_exports(
    *,
    dict_name,
    titles_path,
    rime_path,
    fcitx_path,
    source=None,
    tweaks,
    characters_to_omit=None,
):
    if source is not None and os.environ["AD_BUILD_LOCAL"] == "0":
        s = source
    else:
        s = {
            "file_path": [titles_path],
        }

    if characters_to_omit is None:
        characters_to_omit = []

    return {
        "source": s,
        "tweaks": tweaks,
        "converter": {
            "use": "pypinyin",
            "kwargs": {
                "disable_instinct_pinyin": False,
                "fixfile": FIXFILE_FILE,
                "characters_to_omit": characters_to_omit,
            },
        },
        "generator": [
            {
                "use": "rime",
                "kwargs": {
                    "name": dict_name,
                    "version": BUILD_DATE,
                    "output": rime_path,
                },
            },
            {
                "use": "pinyin",
                "kwargs": {"output": fcitx_path},
            },
        ],
    }
