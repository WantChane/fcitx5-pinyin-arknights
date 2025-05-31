import os
import requests
from bs4 import BeautifulSoup

dict_name, _ext = os.path.splitext(os.path.basename(__file__))

url = "https://prts.wiki/api.php?action=parse&page=萨卡兹的无终奇语/想象实体图鉴&format=json&formatversion=2&utf8=1"
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
            first_tr = table.find("tr")
            if first_tr:
                th_cells = first_tr.find_all("th")
                if len(th_cells) >= 2:
                    title = "".join(
                        th_cells[1].find_all(string=True, recursive=False)
                    ).strip()
                    file.write(title + "\n")

except requests.exceptions.RequestException as e:
    print(f"请求失败：{e}")
except Exception as e:
    print(f"发生错误：{e}")
