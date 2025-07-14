from mw2fcitx.tweaks.moegirl import *
import os
from constant import BUILD_DATE
from custom_tweaks import *


dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250714185549
# 字符 '\n' (U+000A) 出现次数：50
# 字符 '“' (U+201C) 出现次数：8
# 字符 '”' (U+201D) 出现次数：8
# 字符 '(' (U+0028) 出现次数：3
# 字符 ')' (U+0029) 出现次数：3
# 字符 '·' (U+00B7) 出现次数：2
# 字符 '™' (U+2122) 出现次数：2
# endregion

tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_remove_char("™"),
    tweak_find_chinese(),
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
