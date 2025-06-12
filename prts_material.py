from datetime import datetime
from mw2fcitx.tweaks.moegirl import *  # type: ignore
import os
from custom_tweaks import *
from mw2fcitx.version import PKG_VERSION

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

# region
# 20250523144937
# 字符 '-' (U+002D) 出现次数：2
# 字符 '·' (U+00B7) 出现次数：1
# endregion

tweaks = []


exports = {
    "source": {
        "api_path": "https://prts.wiki/api.php",
        "kwargs": {
            "partial": f"output/{dict_name}_partial.json",
            "output": f"output/{dict_name}_titles.txt",
            "request_delay": 2,
            "api_params": {
                "action": "query",
                "cmlimit": "100",
                "cmtitle": "Category:材料",
                "list": "categorymembers",
            },
            "user_agent": f"MW2Fcitx/{PKG_VERSION}; github.com/WantChane/fcitx5-pinyin-prts",
        },
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
