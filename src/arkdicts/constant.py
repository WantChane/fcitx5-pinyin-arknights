import os
from pathlib import Path
from mw2fcitx.version import PKG_VERSION
from datetime import datetime


def get_dict_set(conf_dir):
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


SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent.parent

CONF_DIR = str(SCRIPT_DIR) + "/conf"
OUTPUT_DIR = str(ROOT_DIR) + "/data"

ALL_DICTS = get_dict_set(CONF_DIR)
PRESERVED_PATHS = [
    "fixfile.json",
    "an_other_titles.txt",
]
FIXFILE_FILE = OUTPUT_DIR + "/fixfile.json"

USER_AGENT = f"MW2Fcitx/{PKG_VERSION}; github.com/WantChane/fcitx5-pinyin-arknights"
BUILD_DATE = datetime.now().strftime("%y.%m.%d")
REQUEST_DELAY = 2
MW_LIMIT = "max"
