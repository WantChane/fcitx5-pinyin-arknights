from mw2fcitx.tweaks.moegirl import *
import os
from constant import BUILD_DATE, MW_LIMIT, REQUEST_DELAY, USER_AGENT
from custom_tweaks import *

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250523144854
# 字符 '-' (U+002D) 出现次数：20
# 字符 '(' (U+0028) 出现次数：19
# 字符 ')' (U+0029) 出现次数：19
# 字符 '·' (U+00B7) 出现次数：1
# endregion

tweaks = [
    tweak_trim_parentheses_suffix(),
]


exports = {
    "source": {
        "api_path": "https://prts.wiki/api.php",
        "kwargs": {
            "partial": f"output/{dict_name}_partial.json",
            "output": f"output/{dict_name}_titles.txt",
            "request_delay": REQUEST_DELAY,
            "api_params": {
                "action": "query",
                "cmlimit": MW_LIMIT,
                "cmtitle": "Category:干员",
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
