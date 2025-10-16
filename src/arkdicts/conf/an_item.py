import os
from arkdicts.constant import (
    MW_LIMIT,
    REQUEST_DELAY,
    USER_AGENT,
)
from arkdicts.custom_tweaks import tweak_remove_chars, tweak_find_chinese
from arkdicts.utils.utils import generate_filepath, generate_exports

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)


tweaks = [
    tweak_remove_chars(["“", "”", "《", "》"]),
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
                "cmtitle": "Category:道具",
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
