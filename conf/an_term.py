from mw2fcitx.tweaks.moegirl import *
import os
from constant import BUILD_DATE
from custom_tweaks import *

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

tweaks = [
    tweak_split_word_with(["·"]),
    tweak_mapping({"我方": None}),
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
