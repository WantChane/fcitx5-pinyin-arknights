import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import time
import urllib.parse
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from constant import REQUEST_DELAY, USER_AGENT


def fetch_page_content(
    page_title: str, base_url: str, request_delay: int = 0
) -> BeautifulSoup:
    """获取页面内容并返回BeautifulSoup对象"""
    encoded_title = urllib.parse.quote(page_title)
    api_url = f"{base_url}?action=parse&page={encoded_title}&format=json&formatversion=2&utf8=1"
    headers = {
        "User-Agent": USER_AGENT,
    }

    if request_delay > 0:
        time.sleep(request_delay)
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return BeautifulSoup(data["parse"]["text"], "html.parser")


def extract_text(element, attribute: str, recursive: bool) -> str:
    """从元素中提取文本/属性值"""
    if attribute:
        return element.get(attribute, "").strip()
    return (
        element.get_text(strip=True)
        if recursive
        else "".join(element.find_all(string=True, recursive=False)).strip()
    )


def parse_page(
    page_title: str,
    output_path: str,
    selector: str,
    attribute: str = "",
    base_url: str = "https://prts.wiki/api.php",
    recursive_text: bool = False,
    request_delay: int = 0,
) -> bool:
    """提取页面数据"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        soup = fetch_page_content(page_title, base_url, request_delay)
        elements = soup.select(selector)

        if not elements:
            print(f"未找到匹配选择器 '{selector}' 的元素")
            return False

        texts = [extract_text(el, attribute, recursive_text) + "\n" for el in elements]

        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(texts)

        print(f"成功提取 {len(elements)} 个元素到: {output_path}")
        return True

    except Exception as e:
        print(f"处理错误：{e}")
        return False


def parse_structured_page(
    page_title: str,
    output_path: str,
    selectors: Dict[str, List[str]],
    attributes: Optional[List[str]] = None,
    recursive_texts: Optional[List[bool]] = None,
    delimiter: str = ",",
    base_url: str = "https://prts.wiki/api.php",
    request_delay: int = 0,
) -> bool:
    """提取结构化页面数据"""
    if len(selectors) != 1:
        raise ValueError("selectors 必须包含且仅包含一组根节点选择器")

    root_selector, child_selectors = next(iter(selectors.items()))
    num_children = len(child_selectors)

    # 设置默认值
    attributes = attributes or [""] * num_children
    recursive_texts = recursive_texts or [False] * num_children

    if len(attributes) != num_children or len(recursive_texts) != num_children:
        raise ValueError("属性/递归标志长度需与子节点数一致")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        soup = fetch_page_content(page_title, base_url, request_delay)
        root_elements = soup.select(root_selector)

        if not root_elements:
            print(f"未找到匹配根选择器 '{root_selector}' 的元素")
            return False

        lines = []
        for root in root_elements:
            row = []
            for i, child_selector in enumerate(child_selectors):
                elements = root.select(child_selector)
                if not elements:
                    row.append("")
                    continue

                text = (
                    extract_text(elements[0], attributes[i], recursive_texts[i])
                    .replace("\n", " ")
                    .replace(delimiter, " ")
                )
                row.append(text)

            lines.append(delimiter.join(row) + "\n")

        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"成功提取 {len(root_elements)} 行数据到: {output_path}")
        return True

    except Exception as e:
        print(f"处理错误：{e}")
        return False


if __name__ == "__main__":
    parse_page(
        page_title="刻俄柏的灰蕈迷境/收藏品图鉴",
        output_path="output/an_collection_1_titles.txt",
        selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="傀影与猩红孤钻/长生者宝盒",
        output_path="output/an_collection_2_titles.txt",
        selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="水月与深蓝之树/生物制品陈设",
        output_path="output/an_collection_3_titles.txt",
        selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="探索者的银凇止境/仪式用品索引",
        output_path="output/an_collection_4_titles.txt",
        selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="萨卡兹的无终奇语/想象实体图鉴",
        output_path="output/an_collection_5_titles.txt",
        selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="岁的界园志异/珍玩集册",
        output_path="output/an_collection_6_titles.txt",
        selector="div>table.wikitable>tbody>tr:first-child>th:nth-child(2)",
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="剧情角色一览",
        output_path="output/an_character_titles.txt",
        selector="div>table.wikitable>tbody>tr>td:first-child",
        recursive_text=True,
        request_delay=REQUEST_DELAY,
    )

    parse_structured_page(
        page_title="角色真名",
        output_path="output/an_real_name_titles.txt",
        selectors={
            "div>table.wikitable>tbody>tr:has(td)": [
                "td:nth-child(2)",
                "td:nth-child(3)",
            ]
        },
        recursive_texts=[True, True],
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="泰拉词库",
        output_path="output/an_terra_titles.txt",
        selector="div>table.wikitable>tbody>tr>td:first-child",
        recursive_text=True,
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="时装回廊",
        output_path="output/an_clothes_titles.txt",
        selector=".charnameEn",
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="分支一览",
        output_path="output/an_branch_titles.txt",
        selector="font>strong",
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="干员一览",
        output_path="output/an_operator_v2_titles.txt",
        selector="#filter-data>div",
        attribute="data-zh",
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="道具一览",
        output_path="output/an_item_v2_titles.txt",
        selector="div.smwdata",
        attribute="data-name",
        request_delay=REQUEST_DELAY,
    )

    parse_structured_page(
        page_title="活动一览",
        output_path="output/an_activity_v2_titles.txt",
        selectors={
            "div>table.wikitable>tbody>tr:has(td)": [
                "td:nth-child(2)>a",
                "td:nth-child(3)",
            ]
        },
        recursive_texts=[True, True],
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="术语释义",
        output_path="output/an_term_titles.txt",
        selector="h2~p>b>span",
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="异常效果",
        output_path="output/an_abnormal_titles.txt",
        selector="div>table>tbody>tr>td:nth-child(3)",
        request_delay=REQUEST_DELAY,
    )

    parse_page(
        page_title="召唤物一览",
        output_path="output/an_summons_titles.txt",
        selector="div>table>tbody>tr>td>a",
        request_delay=REQUEST_DELAY,
    )
