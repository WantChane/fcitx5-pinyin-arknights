import argparse
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


TASKS = {
    "an_collection_1": {
        "function": parse_page,
        "args": ["刻俄柏的灰蕈迷境/收藏品图鉴", "output/an_collection_1_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_collection_2": {
        "function": parse_page,
        "args": ["傀影与猩红孤钻/长生者宝盒", "output/an_collection_2_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_collection_3": {
        "function": parse_page,
        "args": ["水月与深蓝之树/生物制品陈设", "output/an_collection_3_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_collection_4": {
        "function": parse_page,
        "args": ["探索者的银凇止境/仪式用品索引", "output/an_collection_4_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_collection_5": {
        "function": parse_page,
        "args": ["萨卡兹的无终奇语/想象实体图鉴", "output/an_collection_5_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_collection_6": {
        "function": parse_page,
        "args": ["岁的界园志异/珍玩集册", "output/an_collection_6_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_character": {
        "function": parse_page,
        "args": ["剧情角色一览", "output/an_character_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr>td:first-child",
            "recursive_text": True,
        },
    },
    "an_real_name": {
        "function": parse_structured_page,
        "args": ["角色真名", "output/an_real_name_titles.txt"],
        "kwargs": {
            "selectors": {
                "div>table.wikitable>tbody>tr:has(td)": [
                    "td:nth-child(2)",
                    "td:nth-child(3)",
                ]
            },
            "recursive_texts": [True, True],
        },
    },
    "an_terra": {
        "function": parse_page,
        "args": ["泰拉词库", "output/an_terra_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr>td:first-child",
            "recursive_text": True,
        },
    },
    "an_clothes": {
        "function": parse_page,
        "args": ["时装回廊", "output/an_clothes_titles.txt"],
        "kwargs": {"selector": ".charnameEn"},
    },
    "an_branch": {
        "function": parse_page,
        "args": ["分支一览", "output/an_branch_titles.txt"],
        "kwargs": {"selector": "font>strong"},
    },
    "an_operator_v2": {
        "function": parse_page,
        "args": ["干员一览", "output/an_operator_v2_titles.txt"],
        "kwargs": {"selector": "#filter-data>div", "attribute": "data-zh"},
    },
    "an_item_v2": {
        "function": parse_page,
        "args": ["道具一览", "output/an_item_v2_titles.txt"],
        "kwargs": {"selector": "div.smwdata", "attribute": "data-name"},
    },
    "an_activity_v2": {
        "function": parse_structured_page,
        "args": ["活动一览", "output/an_activity_v2_titles.txt"],
        "kwargs": {
            "selectors": {
                "div>table.wikitable>tbody>tr:has(td)": [
                    "td:nth-child(2)>a",
                    "td:nth-child(3)",
                ]
            },
            "recursive_texts": [True, True],
        },
    },
    "an_term": {
        "function": parse_page,
        "args": ["术语释义", "output/an_term_titles.txt"],
        "kwargs": {"selector": "h2~p>b>span"},
    },
    "an_abnormal": {
        "function": parse_page,
        "args": ["异常效果", "output/an_abnormal_titles.txt"],
        "kwargs": {"selector": "div>table>tbody>tr>td:nth-child(3)"},
    },
    "an_summons": {
        "function": parse_page,
        "args": ["召唤物一览", "output/an_summons_titles.txt"],
        "kwargs": {"selector": "div>table>tbody>tr>td>a"},
    },
}


def main():
    parser = argparse.ArgumentParser(description="爬取PRTS页面, 生成titles文件")
    parser.add_argument("targets", nargs="*", help="要爬取的词库名 (例如: an_summons)")
    parser.add_argument("--all", action="store_true", help="爬取所有词库")
    args = parser.parse_args()

    if not args.targets and not args.all:
        parser.error("请指定要爬取的词库名或使用 --all 选项")

    if args.all and args.targets:
        parser.error("不能同时使用 --all 和指定词库名")

    request_args = {"request_delay": REQUEST_DELAY}

    if args.all:
        targets = TASKS.keys()
    else:
        targets = args.targets

    for target in targets:
        if target not in TASKS:
            print(f"错误: 未知目标 '{target}'")
            continue

        print(f"正在处理: {target}")
        task = TASKS[target]
        task["function"](*task["args"], **task["kwargs"], **request_args)


if __name__ == "__main__":
    main()
