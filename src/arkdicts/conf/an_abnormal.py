import os
import re
from arkdicts.constant import BUILD_DATE, OUTPUT_DIR, FIXFILE_PATH
from arkdicts.utils.parse_page import parse_page

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path = f"{OUTPUT_DIR}/{dict_name}_titles.txt"
rime_path = f"{OUTPUT_DIR}/{dict_name}.dict.yaml"
fcitx_path = f"{OUTPUT_DIR}/{dict_name}.dict"

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


exports = {
    "source": {
        "file_path": [titles_path],
    },
    "tweaks": tweaks,
    "converter": {
        "use": "pypinyin",
        "kwargs": {
            "disable_instinct_pinyin": False,
            "fixfile": FIXFILE_PATH,
        },
    },
    "generator": [
        {
            "use": "rime",
            "kwargs": {
                "name": dict_name,
                "version": BUILD_DATE,
                "output": rime_path,
            },
        },
        {
            "use": "pinyin",
            "kwargs": {"output": fcitx_path},
        },
    ],
}
