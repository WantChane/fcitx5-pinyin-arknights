import os
from mw2fcitx.version import PKG_VERSION
from datetime import datetime


def get_dict_set(conf_dir="conf"):
    result = set()

    if not os.path.exists(conf_dir):
        return result

    for entry in os.scandir(conf_dir):
        if (
            entry.is_file()
            and entry.name.startswith("an_")
            and entry.name.endswith(".py")
        ):
            filename_without_ext = os.path.splitext(entry.name)[0]
            result.add(filename_without_ext)

    return result


ALL_DICTS = get_dict_set()
MANUAL_DICTS = ["an_other"]
CLEAN_EXCLUDE_FILES = [
    "input/fixfile.json",
    "input/an_other_titles.txt",
    "output/.gitkeep",
]
USER_AGENT = f"MW2Fcitx/{PKG_VERSION}; github.com/WantChane/fcitx5-pinyin-arknights"
BUILD_DATE = datetime.now().strftime("%y.%m.%d")
REQUEST_DELAY = 2
MW_LIMIT = "max"
