import os
import requests
from bs4 import BeautifulSoup

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

url = "https://prts.wiki/api.php?action=parse&page=剧情角色一览&format=json&formatversion=2&utf8=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    soup = BeautifulSoup(data["parse"]["text"], "html.parser")

    with open(f"output/{dict_name}_titles.txt", "w", encoding="utf-8") as file:
        for table in soup.find_all("table", class_="wikitable"):
            for row in table.find_all("tr"):  # type: ignore # type: ignore
                cells = row.find_all(["td", "th"])  # type: ignore
                if len(cells) >= 3:
                    file.write(cells[0].get_text(strip=True) + "\n")

except requests.exceptions.RequestException as e:
    print(f"请求失败：{e}")
except Exception as e:
    print(f"发生错误：{e}")
