import os
from mw2fcitx.tweaks.moegirl import *
from constant import MW_LIMIT, REQUEST_DELAY, USER_AGENT, BUILD_DATE
from custom_tweaks import *

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

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
