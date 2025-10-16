import os
from arkdicts.constant import (
    MW_LIMIT,
    REQUEST_DELAY,
    USER_AGENT,
)
from arkdicts.custom_tweaks import (
    tweak_find_chinese,
    tweak_trim_parentheses_suffix,
    tweak_remove_chars,
    tweak_mapping,
)
from arkdicts.utils.utils import generate_filepath, generate_exports

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

exports = generate_exports(
    source={
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
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
    characters_to_omit=["：", "·"],
)
