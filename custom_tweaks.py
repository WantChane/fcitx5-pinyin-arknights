import re
from typing import List
import regex


def tweak_trim_parentheses_suffix():
    def cb(items: List[str]) -> List[str]:
        pattern = re.compile(r"\s*[（(][^（）)]*[）)]$")
        return [pattern.sub("", item) for item in items]

    return cb


import regex
from typing import List

from typing import List


def tweak_remove_regex_anywhere(regexes):
    from re import compile as regex_compile

    combined_pattern = r"(?:%s)" % "|".join(f"(?:{r})" for r in regexes)
    compiled = regex_compile(combined_pattern)

    def cb(items: List[str]):
        return [s for s in items if not compiled.search(s)]

    return cb


def tweak_remove_pure_chinese():
    def cb(items: List[str]) -> List[str]:
        pattern = regex.compile(r"^\p{Han}+$", regex.UNICODE)
        return [item for item in items if not pattern.fullmatch(item)]

    return cb


def tweak_chinese_with(allowed_chars=None):
    if allowed_chars is None:
        allowed_chars = []
    allowed = re.escape("".join(allowed_chars))
    pattern = re.compile(
        f"([\\u4e00-\\u9fff{allowed}]+)|([^\\u4e00-\\u9fff{allowed}]+)"
    )

    def cb(items: List[str]) -> List[str]:
        result = []
        for item in items:
            parts = []
            for match in pattern.finditer(item):
                chinese_part = match.group(1)
                non_chinese_part = match.group(2)
                if chinese_part:
                    parts.append(chinese_part)
                else:
                    parts.append(non_chinese_part)
            filtered = [p for p in parts if p]
            result.extend(filtered)
        return result

    return cb


if __name__ == "__main__":

    from mw2fcitx.tweaks.moegirl import *  # type: ignore

    def _process_file(input_path: str, output_path: str, tweaks):
        with open(input_path, "r", encoding="utf-8") as f_in:
            input_lines = [line.strip() for line in f_in.readlines()]

        processed = input_lines
        for tweak in tweaks:
            processed = tweak(processed)

        with open(output_path, "w", encoding="utf-8") as f_out:
            f_out.write("\n".join(processed))

    input_file = "input/prts_character_titles.txt"

    tweaks = [
        tweak_remove_char("“"),
        tweak_remove_char("”"),
        tweak_chinese_with(["·", "-"]),
    ]

    output_file = "output/test.txt"
    _process_file(input_file, output_file, tweaks)
