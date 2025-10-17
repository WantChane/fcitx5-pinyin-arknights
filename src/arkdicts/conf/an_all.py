import os
from mw2fcitx.tweaks.moegirl import tweak_trim_suffix
from arkdicts.constant import (
    MW_LIMIT,
    REQUEST_DELAY,
    USER_AGENT,
)
from arkdicts.custom_tweaks import tweak_trim_parentheses_suffix, tweak_find_chinese
from arkdicts.utils.utils import generate_exports, generate_filepath

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)


tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_find_chinese(["·", "-"], connector_only=True),
    tweak_trim_suffix(["·", "-"]),
]

exports = generate_exports(
    source={
        "api_path": "https://prts.wiki/api.php",
        "kwargs": {
            "output": titles_path,
            "request_delay": REQUEST_DELAY,
            "user_agent": USER_AGENT,
            "api_params": {
                "aplimit": MW_LIMIT,
            },
        },
    },
    dict_name=dict_name,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    titles_path=titles_path,
    tweaks=tweaks,
    characters_to_omit=["·", "-"],
)
