from mw2fcitx.tweaks.moegirl import *
import os
from constant import BUILD_DATE
from custom_tweaks import *

dict_name = os.path.splitext(os.path.basename(__file__))

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
        "file_path": [f"input/{dict_name}_titles.txt"],
    },
    "tweaks": tweaks,
    "converter": {
        "use": "pypinyin",
        "kwargs": {
            "disable_instinct_pinyin": False,
            "fixfile": "input/fixfile.json",
            "characters_to_omit": ["·", "-"],
        },
    },
    "generator": [
        {
            "use": "rime",
            "kwargs": {
                "name": dict_name,
                "version": BUILD_DATE,
                "output": f"output/{dict_name}.dict.yaml",
            },
        },
        {
            "use": "pinyin",
            "kwargs": {"output": f"output/{dict_name}.dict"},
        },
    ],
}
