from datetime import datetime
from mw2fcitx.tweaks.moegirl import *
import os
from custom_tweaks import *


dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250611103549
# 字符 '\n' (U+000A) 出现次数：13
# 字符 '#' (U+0023) 出现次数：3
# 字符 ' ' (U+0020) 出现次数：3
# endregion


tweaks = [tweak_ignore_comments()]


exports = {
    "source": {
        "file_path": [f"input/{dict_name}_titles.txt"],
    },
    "tweaks": tweaks,
    "converter": {
        "use": "pypinyin",
        "kwargs": {
            "disable_instinct_pinyin": False,
            "fixfile": "input/fixfile.json",
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
