from datetime import datetime
from mw2fcitx.tweaks.moegirl import *  # type: ignore
import os
from custom_tweaks import *


dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250526184249
# 字符 '·' (U+00B7) 出现次数：107
# 字符 '?' (U+003F) 出现次数：57
# 字符 ' ' (U+0020) 出现次数：52
# 字符 '[' (U+005B) 出现次数：13
# 字符 ']' (U+005D) 出现次数：13
# 字符 '\xa0' (U+00A0) 出现次数：12
# 字符 '"' (U+0022) 出现次数：6
# 字符 '-' (U+002D) 出现次数：4
# 字符 '・' (U+30FB) 出现次数：3
# 字符 '“' (U+201C) 出现次数：3
# 字符 '”' (U+201D) 出现次数：3
# 字符 '（' (U+FF08) 出现次数：1
# 字符 '）' (U+FF09) 出现次数：1
# 字符 "'" (U+0027) 出现次数：1
# endregion

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
