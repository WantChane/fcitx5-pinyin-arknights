from datetime import datetime
from mw2fcitx.tweaks.moegirl import *  # type: ignore
import os
from custom_tweaks import *


dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250603093114
# 字符 ' ' (U+0020) 出现次数：51
# 字符 '.' (U+002E) 出现次数：5
# 字符 '“' (U+201C) 出现次数：2
# 字符 '”' (U+201D) 出现次数：2
# 字符 '/' (U+002F) 出现次数：2
# 字符 '《' (U+300A) 出现次数：1
# 字符 '》' (U+300B) 出现次数：1
# endregion

tweaks = [
    # tweak_trim_parentheses_suffix(),
    tweak_remove_char("“"),
    tweak_remove_char("”"),
    tweak_remove_char("/"),
    tweak_chinese_with(),
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
