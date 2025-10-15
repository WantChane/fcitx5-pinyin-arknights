import click
import re
from collections import Counter


def collect_special_characters(text):
    pattern = r"[^\w\d]|_"
    special_chars = re.findall(pattern, text, flags=re.UNICODE)
    return special_chars


@click.command(name="stat")
@click.argument("file", type=click.Path(exists=True), required=True)
def command(file):
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    special_chars = collect_special_characters(text)
    counter = Counter(special_chars)

    sorted_items = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

    click.echo("-" * 24)
    click.echo(f"{'Char':<5} {'Unicode':<8} {'Frequency':<10}")
    click.echo("-" * 24)

    for char, count in sorted_items:
        hex_code = f"U+{ord(char):04X}"
        char_repr = repr(char)
        click.echo(f"{char_repr:<5} {hex_code:<8} {count:<10}")

    click.echo("-" * 24)
