import os
from arkdicts.constant import BUILD_DATE, FIXFILE_FILE
from mw2fcitx.tweaks.moegirl import tweak_split_word_with, tweak_remove_regex
from arkdicts.custom_tweaks import (
    tweak_delete_by_regex,
    tweak_find_chinese,
    tweak_remove_chars,
)
from arkdicts.utils.parse_page import parse_sequential_page
from arkdicts.utils.utils import generate_filepath

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_sequential_page(
    page_title="活动一览",
    output_path=titles_path,
    selectors=[
        "div>table.wikitable>tbody>tr>td:nth-child(2)>a",
        "div>table.wikitable>tbody>tr>td:nth-child(3)",
    ],
    recursive_texts=[True, True],
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
    tweak_remove_regex(["^第.*章预热$"]),
    tweak_delete_by_regex(["主线动画", "限时任务", "集成回顾"]),
    tweak_remove_chars(["“", "”", "预热", "开放"]),
    tweak_find_chinese("·"),
]


exports = {
    "source": {
        "file_path": [titles_path],
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
