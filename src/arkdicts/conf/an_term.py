import os
from mw2fcitx.tweaks.moegirl import tweak_split_word_with
from arkdicts.custom_tweaks import tweak_mapping
from arkdicts.utils.parse_page import parse_page
from arkdicts.utils.utils import generate_exports, generate_filepath

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_page(
    page_title="术语释义",
    output_path=titles_path,
    selector="h2~p>b>span",
)

tweaks = [
    tweak_split_word_with(["·"]),
    tweak_mapping({"我方": None}),
]

exports = generate_exports(
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
)
