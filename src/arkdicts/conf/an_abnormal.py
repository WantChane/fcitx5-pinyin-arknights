import os
import re
from arkdicts.utils.parse_page import parse_page
from arkdicts.utils.utils import generate_filepath, generate_exports

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path, rime_path, fcitx_path = generate_filepath(dict_name)

parse_page(
    page_title="异常效果",
    output_path=titles_path,
    selector="div>table>tbody>tr>td:nth-child(3)",
)


def process_effects(effects):
    result = []
    pattern = re.compile(r"[$$（]([^$$）]+)[\)）]")

    for effect in effects:
        match = pattern.search(effect)
        if match:
            chinese_word = match.group(1)
            result.append(chinese_word)
            result.append(f"{chinese_word}抗性")
        else:
            result.append(effect)

    return result


tweaks = [
    process_effects,
]

exports = generate_exports(
    dict_name=dict_name,
    titles_path=titles_path,
    rime_path=rime_path,
    fcitx_path=fcitx_path,
    tweaks=tweaks,
)
