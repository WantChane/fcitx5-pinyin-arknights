import datetime
import os
from mw2fcitx.tweaks.moegirl import *  # type: ignore
from custom_tweaks import *
from mw2fcitx.version import PKG_VERSION

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250612132613
# 字符 ' ' (U+0020) 出现次数：500
# 字符 '.' (U+002E) 出现次数：500
# 字符 '\n' (U+000A) 出现次数：500
# 字符 '“' (U+201C) 出现次数：42
# 字符 '”' (U+201D) 出现次数：42
# 字符 '·' (U+00B7) 出现次数：27
# 字符 '！' (U+FF01) 出现次数：23
# 字符 '"' (U+0022) 出现次数：4
# 字符 '(' (U+0028) 出现次数：4
# 字符 ')' (U+0029) 出现次数：4
# 字符 '：' (U+FF1A) 出现次数：3
# 字符 '，' (U+FF0C) 出现次数：2
# endregion

tweaks = [
    lambda words: [word.lstrip("技能 ").rstrip(".png") for word in words],
    tweak_trim_parentheses_suffix(),
    tweak_remove_chars(["“", "”", "！", '"', "，"]),
    tweak_find_chinese(["：", "·"]),
    lambda words: [word.rstrip("·") for word in words],
    tweak_mapping({"型": None}),
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
            "fixfile": f"input/fixfile.json",
            "characters_to_omit": ["：", "·"],
        },
    },
    "generator": [
        {
            "use": "rime",
            "kwargs": {
                "name": dict_name,
                "version": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                "output": f"output/{dict_name}.dict.yaml",
            },
        },
        {
            "use": "pinyin",
            "kwargs": {"output": f"output/{dict_name}.dict"},
        },
    ],
}
