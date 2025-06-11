from datetime import datetime
from mw2fcitx.tweaks.moegirl import *  # type: ignore
import os
from custom_tweaks import *


dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250523144651
# 字符 '/' (U+002F) 出现次数：25
# 字符 '“' (U+201C) 出现次数：4
# 字符 '”' (U+201D) 出现次数：4
# 字符 '×' (U+00D7) 出现次数：2
# 字符 '（' (U+FF08) 出现次数：2
# 字符 '.' (U+002E) 出现次数：2
# 字符 '）' (U+FF09) 出现次数：2
# 字符 '：' (U+FF1A) 出现次数：1
# endregion

tweaks = [
    tweak_remove_chars(["“", "”"]),
    tweak_find_chinese(),
    tweak_delete_by_regex(
        [
            "下载人数突破",
            "端午",
            "限时",
            "签到",
            "登录",
            "公测开服活动",
            "周年",
            "哗啦啦祈愿牌",
            "纪念",
            "预热",
            "庆祝",
            "合作活动",
        ]
    ),
]


exports = {
    "source": {
        "api_path": "https://prts.wiki/api.php",
        "kwargs": {
            "partial": f"output/{dict_name}_partial.json",
            "output": f"output/{dict_name}_titles.txt",
            "request_delay": 2,
            "api_params": {
                "action": "query",
                "cmlimit": "100",
                "cmtitle": "Category:有活动信息的页面",
                "list": "categorymembers",
            },
        },
    },
    "tweaks": tweaks,
    "converter": {
        "use": "pypinyin",
        "kwargs": {
            "disable_instinct_pinyin": False,
            "fixfile": "input/fixfile.json",
            # "characters_to_omit": ["·"],
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
