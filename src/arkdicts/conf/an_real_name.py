import os
from arkdicts.custom_tweaks import (
    tweak_find_chinese,
    tweak_remove_chars,
    tweak_delete_by_regex,
)
from arkdicts.utils.parse_page import parse_sequential_page
from arkdicts.utils.utils import generate_filepath, generate_exports

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_sequential_page(
    page_title="角色真名",
    output_path=titles_path,
    selectors=[
        "div>table.wikitable>tbody>tr>td:nth-child(2)",
        "div>table.wikitable>tbody>tr>td:nth-child(3)",
    ],
    recursive_texts=[True, True],
)

tweaks = [
    lambda words: [
        parts[1] for word in words for parts in [word.split(",")] if len(parts) > 1
    ],
    tweak_remove_chars(
        [
            "“",
            "”",
        ]
    ),
    tweak_find_chinese(["·", "-"]),
    tweak_delete_by_regex([r"\b安心院\b", r"\b真名遗失\b"]),
]

exports = generate_exports(
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
    characters_to_omit=["·", "-"],
)
