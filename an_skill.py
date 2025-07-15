import os
from mw2fcitx.tweaks.moegirl import *
from constant import MW_LIMIT, REQUEST_DELAY, USER_AGENT, BUILD_DATE
from custom_tweaks import *

dict_name = os.path.splitext(os.path.basename(__file__))

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
            "request_delay": REQUEST_DELAY,
            "user_agent": USER_AGENT,
            "api_params": {
                "action": "query",
                "list": "allpages",
                "apnamespace": 6,
                "apprefix": "技能",
                "aplimit": MW_LIMIT,
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
