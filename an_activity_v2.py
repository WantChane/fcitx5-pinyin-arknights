from mw2fcitx.tweaks.moegirl import *
import os
from constant import BUILD_DATE
from custom_tweaks import *

dict_name = os.path.splitext(os.path.basename(__file__))

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
    tweak_delete_by_regex(["主线动画", "限时任务", "集成回顾"]),
    tweak_remove_chars(["“", "”", "预热", "开放"]),
    tweak_find_chinese("·"),
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
