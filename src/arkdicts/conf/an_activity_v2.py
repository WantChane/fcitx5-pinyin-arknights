import os
from mw2fcitx.tweaks.moegirl import tweak_split_word_with
from arkdicts.custom_tweaks import (
    tweak_delete_by_regex,
    tweak_find_chinese,
    tweak_remove_chars,
    tweak_replace_regex,
)
from arkdicts.utils.parse_page import parse_sequential_page
from arkdicts.utils.utils import generate_filepath, generate_exports

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_sequential_page(
    page_title="活动一览",
    output_path=titles_path,
    selectors=[
        "div>table.wikitable>tbody>tr>td:nth-child(2)>a",
        "div>table.wikitable>tbody>tr>td:nth-child(3)",
    ],
)

tweaks = [
    lambda words: [
        parts[0]
        for word in words
        for parts in [word.split(",")]
        if len(parts) > 1
        and not any(
            activity in parts[1]
            for activity in [
                "复刻活动",
                "纪念活动",
                "登录活动",
                "合作活动",
                "愚人节活动",
            ]
        )
    ],
    tweak_split_word_with(["：", "「", "」"]),
    tweak_delete_by_regex(["^第.*章预热$"]),
    tweak_delete_by_regex(["主线动画", "限时任务", "集成回顾"]),
    tweak_remove_chars(["“", "”"]),
    tweak_find_chinese("·"),
    tweak_replace_regex(r"(预热|开放)$"),
]


exports = generate_exports(
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
    characters_to_omit=["·"],
)
