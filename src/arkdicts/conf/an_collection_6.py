import os
from arkdicts.custom_tweaks import tweak_find_chinese, tweak_remove_chars
from arkdicts.utils.utils import generate_filepath, generate_exports
from arkdicts.utils.parse_page import extract_text, parse_page

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_page(
    page_title="岁的界园志异/珍玩集册",
    output_path=titles_path,
    selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
    extractor=extract_text(recursive=False),
)

tweaks = [
    tweak_remove_chars(["“", "”", "《", "》"]),
    tweak_find_chinese(["-", "·"]),
]

exports = generate_exports(
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
    characters_to_omit=["-"],
)
