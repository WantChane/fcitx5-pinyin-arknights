from datetime import datetime
from mw2fcitx.tweaks.moegirl import *  # type: ignore
import os
from custom_tweaks import *


dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250523144651
# 字符 '·' (U+00B7) 出现次数：33
# 字符 ' ' (U+0020) 出现次数：9
# 字符 '！' (U+FF01) 出现次数：7
# 字符 '#' (U+0023) 出现次数：6
# 字符 '：' (U+FF1A) 出现次数：4
# 字符 '“' (U+201C) 出现次数：4
# 字符 '”' (U+201D) 出现次数：4
# 字符 '「' (U+300C) 出现次数：3
# 字符 '」' (U+300D) 出现次数：3
# 字符 '(' (U+0028) 出现次数：2
# 字符 ')' (U+0029) 出现次数：2
# 字符 '×' (U+00D7) 出现次数：2
# 字符 '—' (U+2014) 出现次数：2
# 字符 '.' (U+002E) 出现次数：2
# endregion

tweaks = [
    lambda words: [
        parts[0]
        for word in words
        for parts in [word.split(",")]
        if len(parts) > 1
        and not any(
            activity in parts[1]
            for activity in [
                "复刻活动",
                "纪念活动",
                "登录活动",
                "合作活动",
                "愚人节活动",
            ]
        )
    ],
    tweak_split_word_with(["：", "「", "」"]),
    tweak_remove_regex(["^第.*章预热$"]),
    tweak_remove_regex_anywhere(["主线动画", "限时任务", "集成回顾"]),
    tweak_remove_chars(["“", "”", "预热", "开放"]),
    tweak_chinese_with("·"),
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
            "characters_to_omit": ["·"],
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
