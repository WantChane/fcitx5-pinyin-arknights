import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import requests
from constant import USER_AGENT
from urllib.parse import urlencode

params = {
    "action": "cargoquery",
    "tables": "chara",
    "fields": "chara._pageName=name",
    "where": 'chara.rarity="5"',
    "order_by": "chara.charIndex desc",
    "limit": 1,
    "format": "json",
    "formatversion": 2,
    "utf8": 1,
}

headers = {
    "User-Agent": USER_AGENT,
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
