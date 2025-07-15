import os
import re
from mw2fcitx.tweaks.moegirl import *
from constant import BUILD_DATE
from custom_tweaks import *

dict_name, _ext = os.path.splitext(os.path.basename(__file__))


def process_effects(effects):
    result = []
    pattern = re.compile(r"[$$（]([^$$）]+)[\)）]")

    for effect in effects:
        match = pattern.search(effect)
        if match:
            chinese_word = match.group(1)
            result.append(chinese_word)
            result.append(f"{chinese_word}抗性")
        else:
            result.append(effect)

    return result


tweaks = [
    process_effects,
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
