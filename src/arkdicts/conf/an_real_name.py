import os
from arkdicts.constant import BUILD_DATE, OUTPUT_DIR, FIXFILE_PATH
from arkdicts.custom_tweaks import (
    tweak_find_chinese,
    tweak_remove_chars,
    tweak_delete_by_regex,
)
from arkdicts.utils.parse_page import parse_sequential_page

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path = f"{OUTPUT_DIR}/{dict_name}_titles.txt"
rime_path = f"{OUTPUT_DIR}/{dict_name}.dict.yaml"
fcitx_path = f"{OUTPUT_DIR}/{dict_name}.dict"

parse_sequential_page(
    page_title="角色真名",
    output_path=titles_path,
    selectors=[
        "div>table.wikitable>tbody>tr>td:nth-child(2)",
        "div>table.wikitable>tbody>tr>td:nth-child(3)",
    ],
    recursive_texts=[True, True],
)

tweaks = [
    lambda words: [
        parts[1] for word in words for parts in [word.split(",")] if len(parts) > 1
    ],
    tweak_remove_chars(
        [
            "“",
            "”",
        ]
    ),
    tweak_find_chinese(["·", "-"]),
    tweak_delete_by_regex([r"\b安心院\b", r"\b真名遗失\b"]),
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
            "fixfile": FIXFILE_PATH,
            "characters_to_omit": ["·", "-"],
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
