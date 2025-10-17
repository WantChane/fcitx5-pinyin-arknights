import os
from arkdicts.custom_tweaks import tweak_find_chinese, tweak_remove_chars, tweak_mapping
from arkdicts.utils.parse_page import parse_page
from arkdicts.utils.utils import generate_filepath, generate_exports

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_page(
    page_title="水月与深蓝之树/生物制品陈设",
    output_path=titles_path,
    selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
)

tweaks = [
    tweak_remove_chars(["“", "”", "《", "》"]),
    tweak_find_chinese(["-", "·"]),
    tweak_mapping({"的狙击镜": "狙击镜", "御": None}),
]

exports = generate_exports(
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
    characters_to_omit=["·", "-"],
)
