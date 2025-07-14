from mw2fcitx.tweaks.moegirl import *
import os
from constant import BUILD_DATE, MW_LIMIT, REQUEST_DELAY, USER_AGENT
from custom_tweaks import *

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250603093114
# 字符 '（' (U+FF08) 出现次数：47
# 字符 '）' (U+FF09) 出现次数：47
# 字符 '“' (U+201C) 出现次数：24
# 字符 '”' (U+201D) 出现次数：24
# 字符 '-' (U+002D) 出现次数：13
# 字符 '·' (U+00B7) 出现次数：7
# 字符 '《' (U+300A) 出现次数：5
# 字符 '》' (U+300B) 出现次数：5
# 字符 '★' (U+2605) 出现次数：2
# 字符 '!' (U+0021) 出现次数：2
# 字符 '！' (U+FF01) 出现次数：1
# 字符 ':' (U+003A) 出现次数：1
# endregion

tweaks = [
    tweak_remove_chars(["“", "”", "《", "》"]),
    tweak_find_chinese(["·", "-"]),
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
                "cmtitle": "Category:道具",
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
