import os
from mw2fcitx.tweaks.moegirl import *
from constant import USER_AGENT, BUILD_DATE
from custom_tweaks import *

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 字符 ' ' (U+0020) 出现次数：1280
# 字符 ':' (U+003A) 出现次数：1127
# 字符 '.' (U+002E) 出现次数：1127
# 字符 '\n' (U+000A) 出现次数：1126
# 字符 '·' (U+00B7) 出现次数：71
# 字符 '“' (U+201C) 出现次数：50
# 字符 '”' (U+201D) 出现次数：50
# 字符 '！' (U+FF01) 出现次数：36
# 字符 '-' (U+002D) 出现次数：13
# 字符 '(' (U+0028) 出现次数：7
# 字符 ')' (U+0029) 出现次数：7
# 字符 '：' (U+FF1A) 出现次数：6
# 字符 '，' (U+FF0C) 出现次数：5
# 字符 '"' (U+0022) 出现次数：4
# 字符 '？' (U+FF1F) 出现次数：2
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
        "api_path": "https://prts.wiki/api.php",
        "kwargs": {
            "partial": f"output/{dict_name}_partial.json",
            "output": f"output/{dict_name}_titles.txt",
            "request_delay": 2,
            "user_agent": USER_AGENT,
            "api_params": {
                "action": "query",
                "list": "allpages",
                "apnamespace": 6,
                "apprefix": "技能",
                "aplimit": "max",
            },
        },
        # "file_path": [f"input/{dict_name}_titles.txt"],
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
