import os
from arkdicts.custom_tweaks import tweak_trim_parentheses_suffix, tweak_find_chinese
from arkdicts.utils.parse_page import parse_page
from arkdicts.utils.utils import generate_filepath, generate_exports

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_page(
    page_title="泰拉词库",
    output_path=titles_path,
    selector="div>table.wikitable>tbody>tr>td:first-child",
)

tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_find_chinese(["·", "B", "-"]),
]

exports = generate_exports(
    dict_name=dict_name,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    titles_path=titles_path,
    tweaks=tweaks,
    characters_to_omit=["·", "B", "-"],
)
