from mw2fcitx.version import PKG_VERSION
from datetime import datetime

USER_AGENT = f"MW2Fcitx/{PKG_VERSION}; github.com/WantChane/fcitx5-pinyin-prts"
BUILD_DATE = datetime.now().strftime("%y.%m.%d")
REQUEST_DELAY = 2
MW_LIMIT = "max"
