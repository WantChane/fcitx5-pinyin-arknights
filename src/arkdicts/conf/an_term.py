import os
from mw2fcitx.tweaks.moegirl import tweak_split_word_with
from arkdicts.constant import BUILD_DATE, OUTPUT_DIR, FIXFILE_PATH
from arkdicts.custom_tweaks import tweak_mapping
from arkdicts.utils.parse_page import parse_page

dict_name = os.path.splitext(os.path.basename(__file__))[0]
titles_path = f"{OUTPUT_DIR}/{dict_name}_titles.txt"
rime_path = f"{OUTPUT_DIR}/{dict_name}.dict.yaml"
fcitx_path = f"{OUTPUT_DIR}/{dict_name}.dict"

parse_page(
    page_title="术语释义",
    output_path=titles_path,
    selector="h2~p>b>span",
)

tweaks = [
    tweak_split_word_with(["·"]),
    tweak_mapping({"我方": None}),
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
