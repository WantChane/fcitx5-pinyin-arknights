from mw2fcitx.tweaks.moegirl import *
import os
from constant import BUILD_DATE, USER_AGENT
from custom_tweaks import *

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250523145024
# 字符 '“' (U+201C) 出现次数：221
# 字符 '”' (U+201D) 出现次数：221
# 字符 '，' (U+FF0C) 出现次数：38
# 字符 '·' (U+00B7) 出现次数：21
# 字符 '-' (U+002D) 出现次数：19
# 字符 '(' (U+0028) 出现次数：16
# 字符 ')' (U+0029) 出现次数：16
# 字符 '!' (U+0021) 出现次数：2
# endregion

tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_split_word_with(["“", "”", "，"]),
    tweak_find_chinese(["·", "-"]),
]


exports = {
    "source": {
        "api_path": "https://prts.wiki/api.php",
        # "file_path": [f"input/f{dict_name}_titles.txt"],
        "kwargs": {
            "partial": f"output/{dict_name}_partial.json",
            "output": f"output/{dict_name}_titles.txt",
            "request_delay": 2,
            "api_params": {
                "action": "query",
                "cmlimit": "100",
                "cmtitle": "Category:敌人",
                "list": "categorymembers",
            },
            "user_agent": USER_AGENT,
        },
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
