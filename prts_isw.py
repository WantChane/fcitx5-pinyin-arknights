from datetime import datetime
from mw2fcitx.tweaks.moegirl import *  # type: ignore
import os
from custom_tweaks import *
from mw2fcitx.version import PKG_VERSION

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250523145024
# 字符 '-' (U+002D) 出现次数：284
# 字符 ' ' (U+0020) 出现次数：284
# 字符 '\n' (U+000A) 出现次数：283
# 字符 '(' (U+0028) 出现次数：5
# 字符 ')' (U+0029) 出现次数：5
# 字符 '“' (U+201C) 出现次数：5
# 字符 '”' (U+201D) 出现次数：5
# 字符 '?' (U+003F) 出现次数：3
# endregion

tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_remove_chars(["“", "”"]),
    tweak_find_chinese(),
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
                "cmtitle": "Category:集成战略关卡",
                "list": "categorymembers",
            },
            "user_agent": f"MW2Fcitx/{PKG_VERSION}; github.com/WantChane/fcitx5-pinyin-prts",
        },
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
