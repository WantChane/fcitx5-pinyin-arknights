from datetime import datetime
from mw2fcitx.tweaks.moegirl import *  # type: ignore
import os
from custom_tweaks import *


dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250526213741
# 字符 '/' (U+002F) 出现次数：104
# 字符 '·' (U+00B7) 出现次数：73
# 字符 '“' (U+201C) 出现次数：19
# 字符 '”' (U+201D) 出现次数：19
# 字符 '（' (U+FF08) 出现次数：4
# 字符 '）' (U+FF09) 出现次数：4
# 字符 '.' (U+002E) 出现次数：4
# 字符 '？' (U+FF1F) 出现次数：3
# 字符 '，' (U+FF0C) 出现次数：2
# 字符 ' ' (U+0020) 出现次数：2
# 字符 '&' (U+0026) 出现次数：1
# endregion

tweaks = [
    tweak_chinese_with(["·"]),
    tweak_remove_regex_anywhere([r"\b医疗\b", r"\b代号\b", r"\b名称\b", r"\b的父亲\b"]),
]


exports = {
    "source": {
        "file_path": [f"input/{dict_name}_titles.txt"],
    },
    "tweaks": tweaks,
    "converter": {
        "use": "opencc",
        "kwargs": {
            "disable_instinct_pinyin": False,
            "fixfile": "input/fixfile.json",
            "characters_to_omit": ["·", "B", "-"],
        },
    },
    "generator": [
        {
            "use": "rime",
            "kwargs": {
                "name": dict_name,
                "version": datetime.now().strftime("%Y%m%d%H%M%S"),
                "output": f"output/{dict_name}.dict.yaml",
            },
        },
        {
            "use": "pinyin",
            "kwargs": {"output": f"output/{dict_name}.dict"},
        },
    ],
}
