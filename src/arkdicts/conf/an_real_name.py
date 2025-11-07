import re
import os
from arkdicts.custom_tweaks import (
    tweak_find_chinese,
    tweak_remove_chars,
)
from mw2fcitx.tweaks.moegirl import tweak_opencc_t2s
from arkdicts.utils.parse_page import (
    SEMANTIC_BLOCK_TAGS,
    SEMANTIC_INLINE_TAGS,
    extract_text,
    parse_sequential_page,
    semantic_extract_text,
)
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
    extractor=[
        extract_text(),
        semantic_extract_text(
            inline_tags=SEMANTIC_INLINE_TAGS - {"span"},
            block_tags=SEMANTIC_BLOCK_TAGS | {"span"},
        ),
    ],
)


def tweak_remove_parentheses():
    def remove_parentheses(items: list[str]) -> list[str]:
        pattern = re.compile(r"\s*[（({\[][^（）)}\]\]]*?[）)}\]\]]")
        return [pattern.sub("", item) for item in items]

    return remove_parentheses


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
    lambda words: [item for s in words for item in s.split("|")],
    tweak_remove_parentheses(),
    tweak_find_chinese(["·", "-"], connector_only=True, strict=True),
    tweak_opencc_t2s,
]

exports = generate_exports(
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
    characters_to_omit=["·", "-"],
)
