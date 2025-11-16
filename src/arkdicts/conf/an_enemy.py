import os
from mw2fcitx.tweaks.moegirl import tweak_split_word_with
from arkdicts.constant import (
    MW_LIMIT,
    REQUEST_DELAY,
    USER_AGENT,
)
from arkdicts.custom_tweaks import tweak_find_chinese, tweak_trim_parentheses_suffix
from arkdicts.utils.utils import generate_filepath, generate_exports

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)


tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_split_word_with(["“", "”", "，"]),
    tweak_find_chinese(["·", "-"]),
]

exports = generate_exports(
    source={
        "api_path": "https://prts.wiki/api.php",
        "kwargs": {
            "output": titles_path,
            "request_delay": REQUEST_DELAY,
            "api_params": {
                "action": "query",
                "cmlimit": MW_LIMIT,
                "cmtitle": "Category:敌人",
                "list": "categorymembers",
            },
            "user_agent": USER_AGENT,
        },
    },
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
    characters_to_omit=["·", "-"],
)
