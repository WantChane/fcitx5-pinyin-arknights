import os
from arkdicts.constant import (
    MW_LIMIT,
    REQUEST_DELAY,
    USER_AGENT,
    BUILD_DATE,
    FIXFILE_FILE,
)
from arkdicts.custom_tweaks import (
    tweak_find_chinese,
    tweak_trim_parentheses_suffix,
    tweak_remove_chars,
    tweak_mapping,
)
from arkdicts.utils.utils import generate_filepath

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

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
            "output": titles_path,
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
    },
    "tweaks": tweaks,
    "converter": {
        "use": "pypinyin",
        "kwargs": {
            "disable_instinct_pinyin": False,
            "fixfile": FIXFILE_FILE,
            "characters_to_omit": ["：", "·"],
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
