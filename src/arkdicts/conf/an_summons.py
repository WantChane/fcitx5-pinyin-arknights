import os
from mw2fcitx.tweaks.moegirl import tweak_remove_char
from arkdicts.custom_tweaks import tweak_trim_parentheses_suffix, tweak_find_chinese
from arkdicts.utils.parse_page import parse_page
from arkdicts.utils.utils import generate_filepath, generate_exports

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_page(
    page_title="召唤物一览",
    output_path=titles_path,
    selector="div>table>tbody>tr>td>a",
)

tweaks = [
    tweak_trim_parentheses_suffix(),
    tweak_remove_char("™"),
    tweak_find_chinese(),
]

exports = generate_exports(
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
)
