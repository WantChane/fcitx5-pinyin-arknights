import os
from arkdicts.utils.parse_page import parse_page
from arkdicts.utils.utils import generate_filepath, generate_exports

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_page(
    page_title="分支一览",
    output_path=titles_path,
    selector="font>strong",
    recursive_text=True,
)

tweaks = []

exports = generate_exports(
    source={
        "file_path": [titles_path],
    },
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
)
