import requests
from mw2fcitx.version import PKG_VERSION
from urllib.parse import urlencode
import os
import sys

params = {
    "action": "cargoquery",
    "tables": "char_obtain,chara",
    "fields": "char_obtain._pageName=name",
    "where": 'chara.rarity="5"',
    "join_on": "char_obtain._pageName=chara._pageName",
    "order_by": "char_obtain.cnOnlineTime desc",
    "limit": 1,
    "format": "json",
    "formatversion": 2,
    "utf8": 1,
}

headers = {
    "User-Agent": f"MW2Fcitx/{PKG_VERSION}; github.com/WantChane/fcitx5-pinyin-prts",
}

try:
    response = requests.get(
        f"https://prts.wiki/api.php?{urlencode(params)}",
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    current_version = data["cargoquery"][0]["title"]["name"]

    version_file = "VERSION"
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            old_version = f.read().strip()
    else:
        old_version = None

    version_changed = current_version != old_version

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
            fh.write(f"changed={str(version_changed).lower()}\n")
            fh.write(f"current_version={current_version}\n")
    else:
        print(f"changed={str(version_changed).lower()}")
        print(f"current_version={current_version}")

    if version_changed:
        with open(version_file, "w") as f:
            f.write(current_version)
        print(f"version changed: {old_version or 'None'} → {current_version}")
    else:
        print(f"version unchanged: {current_version}")

    sys.exit(0)

except requests.exceptions.RequestException as e:
    print(f"API请求失败: {str(e)}", file=sys.stderr)
    sys.exit(2)
except (KeyError, IndexError) as e:
    print(f"JSON解析错误: {str(e)}", file=sys.stderr)
    sys.exit(3)
