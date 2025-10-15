import os
from arkdicts.constant import (
    BUILD_DATE,
    OUTPUT_DIR,
    FIXFILE_PATH,
    MW_LIMIT,
    REQUEST_DELAY,
    USER_AGENT,
)
from arkdicts.custom_tweaks import (
    tweak_trim_parentheses_suffix,
    tweak_remove_chars,
    tweak_find_chinese,
)

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path = f"{OUTPUT_DIR}/{dict_name}_titles.txt"
rime_path = f"{OUTPUT_DIR}/{dict_name}.dict.yaml"
fcitx_path = f"{OUTPUT_DIR}/{dict_name}.dict"
partial_path = f"{OUTPUT_DIR}/{dict_name}_partial.json"

tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_remove_chars(["“", "”", "·", "，"]),
    tweak_find_chinese(),
]

exports = {
    "source": {
        "api_path": "https://prts.wiki/api.php",
        "kwargs": {
            "partial": partial_path,
            "output": titles_path,
            "request_delay": REQUEST_DELAY,
            "api_params": {
                "action": "query",
                "cmlimit": MW_LIMIT,
                "cmtitle": "Category:集成战略关卡",
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
            "fixfile": FIXFILE_PATH,
        },
    },
    "generator": [
        {
            "use": "rime",
            "kwargs": {
                "name": dict_name,
                "version": BUILD_DATE,
                "output": rime_path,
            },
        },
        {
            "use": "pinyin",
            "kwargs": {"output": fcitx_path},
        },
    ],
}
