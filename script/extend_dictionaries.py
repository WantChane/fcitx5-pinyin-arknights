import os
import urllib.parse
import requests
from bs4 import BeautifulSoup


def parse_tables(
    page_title: str,
    output_path: str,
    selector: str,
    base_url: str = "https://prts.wiki/api.php",
    recursive_text: bool = False,
):
    """
    使用CSS选择器提取MediaWiki页面中表格的指定单元格数据并保存到文件

    参数:
        page_title: 要抓取的页面标题
        output_path: 输出文件路径
        selector: CSS选择器表达式,用于定位目标元素
        base_url: MediaWiki站点基础URL (默认"https://prts.wiki/api.php")
        recursive_text: 是否递归提取所有文本 (默认False)
    """
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 构建API请求URL
    encoded_title = urllib.parse.quote(page_title)
    api_url = f"{base_url}?action=parse&page={encoded_title}&format=json&formatversion=2&utf8=1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        html_content = data["parse"]["text"]

        soup = BeautifulSoup(html_content, "html.parser")

        elements = soup.select(selector)

        if not elements:
            print(f"未找到匹配选择器 '{selector}' 的元素")
            return False

        texts = []
        for element in elements:
            if recursive_text:
                text = element.get_text(strip=True)
            else:
                text = "".join(
                    element.find_all(string=True, recursive=False)  # type: ignore
                ).strip()

            texts.append(text + "\n")

        with open(output_path, "w", encoding="utf-8") as file:
            file.writelines(texts)

        print(f"成功提取 {len(elements)} 个元素到: {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
    except KeyError as e:
        print(f"JSON解析错误：{e}")
    except Exception as e:
        print(f"处理错误：{e}")

    return False


parse_tables(
    page_title="刻俄柏的灰蕈迷境/收藏品图鉴",
    output_path="output/prts_collection_1_titles.txt",
    selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
)

parse_tables(
    page_title="傀影与猩红孤钻/长生者宝盒",
    output_path="output/prts_collection_2_titles.txt",
    selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
)

parse_tables(
    page_title="水月与深蓝之树/生物制品陈设",
    output_path="output/prts_collection_3_titles.txt",
    selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
)

parse_tables(
    page_title="探索者的银凇止境/仪式用品索引",
    output_path="output/prts_collection_4_titles.txt",
    selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
)

parse_tables(
    page_title="萨卡兹的无终奇语/想象实体图鉴",
    output_path="output/prts_collection_5_titles.txt",
    selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
)

parse_tables(
    page_title="剧情角色一览",
    output_path="output/prts_character_titles.txt",
    selector="div>table.wikitable>tbody>tr>td:first-child",
    recursive_text=True,
)

parse_tables(
    page_title="角色真名",
    output_path="output/prts_real_name_titles.txt",
    selector="div>table.wikitable>tbody>tr>td:nth-child(3)",
    recursive_text=True,
)

parse_tables(
    page_title="泰拉词库",
    output_path="output/prts_terra_titles.txt",
    selector="div>table.wikitable>tbody>tr>td:first-child",
    recursive_text=True,
)
