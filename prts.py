# By default we assume the configuration is located at a variable
#     called "exports".
# You can change this with `-n any_name` in the CLI.

import datetime
from mw2fcitx.tweaks.moegirl import *

tweaks = [
    tweak_remove_word_includes(["○", "〇"]),
    tweak_split_word_with(
        [":", "/", "(", ")", "（", "）", "【", "】", "『", "』", "／", " ", "!", "！"]
    ),
    tweak_len_more_than(1),
    tweak_remove_char("·"),
    tweak_trim_suffix(["系列", "列表", "对照表", "的信物", "的中坚信物"]),
    tweak_remove_regex(["^第.*(次|话)$"]),
    tweak_normalize,
]


exports = {
    # Source configurations.
    "source": {
        # MediaWiki api.php path, if to fetch titles from online.
        "api_path": "https://prts.wiki/api.php",
        # Title file path, if to fetch titles from local file. (optional)
        # Can be a path or a list of paths.
        "file_path": ["titles.txt"],
        "kwargs": {
            # Title number limit for fetching. (optional)
            # "title_limit": 120,
            # Title number limit for fetching via API. (optional)
            # Overrides title_limit.
            # "api_title_limit": 120,
            # Title number limit for each fetch via file. (optional)
            # Overrides title_limit.
            # "file_title_limit": 60,
            # Partial session file on exception (optional)
            "partial": "partial.json",
            # Title list export path. (optional)
            "output": "titles.txt",
            # Delay between MediaWiki API requests in seconds. (optional)
            "request_delay": 2,
            # Results per API request; same as `aplimit` in MediaWiki docs. (optional)
            "aplimit": "max",
        },
    },
    # Tweaks configurations as an list.
    # Every tweak function accepts a list of titles and return
    #     a list of title.
    "tweaks": tweaks,
    # Converter configurations.
    "converter": {
        # opencc is a built-in converter.
        # For custom converter functions, just give the function itself.
        "use": "opencc",
        "kwargs": {
            # Replace "m" to "mu" and "n" to "en". Default: False.
            # See more in https://github.com/outloudvi/mw2fcitx/issues/29 .
            "disable_instinct_pinyin": False,
            # Pinyin results to replace. (optional)
            # Format: { "汉字": "pin'yin" }
            "fixfile": "fixfile.json",
        },
    },
    # Generator configurations.
    "generator": [
        {
            # rime is a built-in generator.
            # For custom generator functions, just give the function itself.
            "use": "rime",
            "kwargs": {
                # Destination dictionary filename. (optional)
                "name": "prts",
                "version": datetime.datetime.now().strftime("%Y-%m-%d"),
                "output": "prts.dict.yaml",
            },
        },
        {
            # pinyin is a built-in generator.
            # This generator depends on `libime`.
            "use": "pinyin",
            "kwargs": {
                # Destination dictionary filename. (mandatory)
                "output": "prts.dict"
            },
        },
    ],
}
