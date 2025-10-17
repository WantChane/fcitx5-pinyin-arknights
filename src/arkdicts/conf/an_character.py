import os
from arkdicts.custom_tweaks import (
    tweak_trim_parentheses_suffix,
    tweak_remove_chars,
    tweak_find_chinese,
    tweak_delete_by_regex,
)
from arkdicts.utils.parse_page import parse_page
from arkdicts.utils.utils import generate_filepath, generate_exports

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_page(
    page_title="剧情角色一览",
    output_path=titles_path,
    selector="div>table.wikitable>tbody>tr>td:first-child",
    recursive_text=True,
)

tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_remove_chars(["“", "”"]),
    tweak_find_chinese(["·"]),
    tweak_delete_by_regex(["父亲", "母亲"]),
]

exports = generate_exports(
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
    characters_to_omit=["·", "B", "-"],
)
