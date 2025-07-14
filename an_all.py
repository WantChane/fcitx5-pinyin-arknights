import os
from mw2fcitx.tweaks.moegirl import *
from constant import MW_LIMIT, REQUEST_DELAY, USER_AGENT, BUILD_DATE
from custom_tweaks import *

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250603144541
# 字符 '-' (U+002D) 出现次数：8466
# 字符 ' ' (U+0020) 出现次数：7420
# 字符 '/' (U+002F) 出现次数：6102
# 字符 '“' (U+201C) 出现次数：1037
# 字符 '”' (U+201D) 出现次数：1033
# 字符 '(' (U+0028) 出现次数：358
# 字符 ')' (U+0029) 出现次数：358
# 字符 '·' (U+00B7) 出现次数：260
# 字符 '.' (U+002E) 出现次数：226
# 字符 '，' (U+FF0C) 出现次数：189
# 字符 '（' (U+FF08) 出现次数：151
# 字符 '）' (U+FF09) 出现次数：151
# 字符 '《' (U+300A) 出现次数：114
# 字符 '》' (U+300B) 出现次数：114
# 字符 '！' (U+FF01) 出现次数：61
# 字符 ':' (U+003A) 出现次数：58
# 字符 '：' (U+FF1A) 出现次数：53
# 字符 '?' (U+003F) 出现次数：27
# 字符 '？' (U+FF1F) 出现次数：25
# 字符 '™' (U+2122) 出现次数：20
# 字符 '"' (U+0022) 出现次数：15
# 字符 '・' (U+30FB) 出现次数：13
# 字符 '、' (U+3001) 出现次数：12
# 字符 '!' (U+0021) 出现次数：10
# 字符 '&' (U+0026) 出现次数：7
# 字符 "'" (U+0027) 出现次数：7
# 字符 '—' (U+2014) 出现次数：6
# 字符 ',' (U+002C) 出现次数：4
# 字符 '*' (U+002A) 出现次数：4
# 字符 '≧' (U+2267) 出现次数：2
# 字符 '▽' (U+25BD) 出现次数：2
# 字符 '≦' (U+2266) 出现次数：2
# 字符 '★' (U+2605) 出现次数：2
# 字符 '×' (U+00D7) 出现次数：2
# 字符 '…' (U+2026) 出现次数：2
# 字符 '⁻' (U+207B) 出现次数：1
# 字符 '「' (U+300C) 出现次数：1
# 字符 '」' (U+300D) 出现次数：1
# endregion

tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_find_chinese(["·", "-"]),
    tweak_trim_suffix(["·", "-"]),
]


exports = {
    "source": {
        "api_path": "https://prts.wiki/api.php",
        "kwargs": {
            "partial": f"output/{dict_name}_partial.json",
            "output": f"output/{dict_name}_titles.txt",
            "request_delay": REQUEST_DELAY,
            "user_agent": USER_AGENT,
            "api_params": {
                "aplimit": MW_LIMIT,
            },
        },
    },
    "tweaks": tweaks,
    "converter": {
        "use": "pypinyin",
        "kwargs": {
            "disable_instinct_pinyin": False,
            "fixfile": f"input/fixfile.json",
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
