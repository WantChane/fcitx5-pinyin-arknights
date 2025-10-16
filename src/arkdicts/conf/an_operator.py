import os
from arkdicts.constant import (
    BUILD_DATE,
    MW_LIMIT,
    REQUEST_DELAY,
    FIXFILE_FILE,
    USER_AGENT,
)
from arkdicts.custom_tweaks import tweak_trim_parentheses_suffix
from arkdicts.utils.utils import generate_filepath

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)


tweaks = [
    tweak_trim_parentheses_suffix(),
]

exports = {
    "source": {
        "api_path": "https://prts.wiki/api.php",
        "kwargs": {
            "output": titles_path,
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
            "fixfile": FIXFILE_FILE,
            "characters_to_omit": ["·"],
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
