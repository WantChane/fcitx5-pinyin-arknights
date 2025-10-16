import os
from arkdicts.constant import BUILD_DATE, FIXFILE_FILE
from arkdicts.custom_tweaks import (
    tweak_trim_parentheses_suffix,
    tweak_remove_chars,
    tweak_find_chinese,
    tweak_mapping,
)
from arkdicts.utils.parse_page import parse_page
from arkdicts.utils.utils import generate_filepath

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_page(
    page_title="剧情角色一览",
    output_path=titles_path,
    selector="div>table.wikitable>tbody>tr>td:first-child",
    recursive_text=True,
)

tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_remove_chars(["“", "”"]),
    tweak_find_chinese(["·"]),
    tweak_mapping({"的父亲": None}),
]

exports = {
    "source": {
        "file_path": [titles_path],
    },
    "tweaks": tweaks,
    "converter": {
        "use": "pypinyin",
        "kwargs": {
            "disable_instinct_pinyin": False,
            "fixfile": FIXFILE_FILE,
            "characters_to_omit": ["·", "B", "-"],
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
