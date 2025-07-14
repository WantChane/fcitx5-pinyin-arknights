from mw2fcitx.tweaks.moegirl import *
import os
from constant import BUILD_DATE
from custom_tweaks import *


dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250526213741
# 字符 '·' (U+00B7) 出现次数：27
# 字符 '/' (U+002F) 出现次数：9
# 字符 '.' (U+002E) 出现次数：4
# 字符 '-' (U+002D) 出现次数：2
# 字符 '(' (U+0028) 出现次数：1
# 字符 ')' (U+0029) 出现次数：1
# endregion

tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_find_chinese(["·", "B", "-"]),
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
            "characters_to_omit": ["·", "B", "-"],
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
