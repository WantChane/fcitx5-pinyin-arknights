from datetime import datetime
from mw2fcitx.tweaks.moegirl import *  # type: ignore
import os
from custom_tweaks import *


dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250610124705
# 字符 '\n' (U+000A) 出现次数：53
# 字符 '（' (U+FF08) 出现次数：9
# 字符 '）' (U+FF09) 出现次数：9
# 字符 '×' (U+00D7) 出现次数：2
# 字符 '_' (U+005F) 出现次数：1
# endregion
import re


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
                "version": datetime.now().strftime("%Y%m%d%H%M%S"),
                "output": f"output/{dict_name}.dict.yaml",
            },
        },
        {
            "use": "pinyin",
            "kwargs": {"output": f"output/{dict_name}.dict"},
        },
    ],
}
