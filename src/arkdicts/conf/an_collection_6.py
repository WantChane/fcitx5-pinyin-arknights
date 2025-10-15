import os
from arkdicts.constant import BUILD_DATE, OUTPUT_DIR, FIXFILE_PATH
from arkdicts.custom_tweaks import tweak_find_chinese, tweak_remove_chars
from arkdicts.utils.parse_page import parse_page

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path = f"{OUTPUT_DIR}/{dict_name}_titles.txt"
rime_path = f"{OUTPUT_DIR}/{dict_name}.dict.yaml"
fcitx_path = f"{OUTPUT_DIR}/{dict_name}.dict"

parse_page(
    page_title="岁的界园志异/珍玩集册",
    output_path=titles_path,
    selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
)

tweaks = [
    tweak_remove_chars(["“", "”", "《", "》"]),
    tweak_find_chinese(["-", "·"]),
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
            "characters_to_omit": ["-"],
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
