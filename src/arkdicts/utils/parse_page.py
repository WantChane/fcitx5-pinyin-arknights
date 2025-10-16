import os
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from arkdicts.constant import USER_AGENT, REQUEST_DELAY


def fetch_page_content(
    page_title: str, base_url: str, request_delay: int = REQUEST_DELAY
) -> BeautifulSoup:
    """获取页面内容并返回BeautifulSoup对象"""
    if os.environ["AD_BUILD_LOCAL"] == "1":
        raise EnvironmentError()

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
    request_delay: int = REQUEST_DELAY,
) -> bool:
    """提取页面数据"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        soup = fetch_page_content(page_title, base_url, request_delay)
        elements = soup.select(selector)

        if not elements:
            print(f"No elements found matching selector '{selector}'")
            return False

        texts = [extract_text(el, attribute, recursive_text) + "\n" for el in elements]

        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(texts)

        print(f"Successfully extracted {len(elements)} elements to: {output_path}")
        return True

    except EnvironmentError:
        return False
    except Exception as e:
        print(f"Processing error: {e}")
        return False


def parse_structured_page(
    page_title: str,
    output_path: str,
    selectors: Dict[str, List[str]],
    attributes: Optional[List[str]] = None,
    recursive_texts: Optional[List[bool]] = None,
    delimiter: str = ",",
    base_url: str = "https://prts.wiki/api.php",
    request_delay: int = REQUEST_DELAY,
) -> bool:
    """提取结构化页面数据"""
    if len(selectors) != 1:
        raise ValueError(
            "Selectors must contain and only contain a set of root node selectors"
        )

    root_selector, child_selectors = next(iter(selectors.items()))
    num_children = len(child_selectors)

    attributes = attributes or [""] * num_children
    recursive_texts = recursive_texts or [False] * num_children

    if len(attributes) != num_children or len(recursive_texts) != num_children:
        raise ValueError(
            "The length of the attributes and recursive_texts flag must match the number of selectors."
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        soup = fetch_page_content(page_title, base_url, request_delay)
        root_elements = soup.select(root_selector)

        if not root_elements:
            print(f"No elements found matching root selector '{root_selector}'")
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

        print(f"Successfully extracted {len(root_elements)} rows to: {output_path}")
        return True

    except EnvironmentError:
        return False
    except Exception as e:
        print(f"Processing error: {e}")
        return False


def parse_sequential_page(
    page_title: str,
    output_path: str,
    selectors: List[str],
    attributes: List[str] = [],
    recursive_texts: List[bool] = [],
    delimiter: str = ",",
    base_url: str = "https://prts.wiki/api.php",
    request_delay: int = REQUEST_DELAY,
) -> bool:
    num_selectors = len(selectors)
    attributes = attributes or [""] * num_selectors
    recursive_texts = recursive_texts or [False] * num_selectors

    if len(attributes) != num_selectors or len(recursive_texts) != num_selectors:
        raise ValueError(
            "The length of the attributes and recursive_texts flag must match the number of selectors."
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        soup = fetch_page_content(page_title, base_url, request_delay)

        selector_elements = []
        for selector in selectors:
            elements = soup.select(selector)
            selector_elements.append(elements)

            if not elements:
                print(f"No elements found for selector '{selector}'")
            else:
                print(f"Selector '{selector}' matched {len(elements)} elements")

        all_matches = []
        for selector_idx, elements in enumerate(selector_elements):
            for element in elements:
                sourceline = getattr(element, "sourceline", float("inf"))
                sourcepos = getattr(element, "sourcepos", float("inf"))

                all_matches.append(
                    {
                        "sourceline": sourceline,
                        "sourcepos": sourcepos,
                        "selector_idx": selector_idx,
                        "element": element,
                    }
                )

        if not all_matches:
            print("No selectors matched any elements")
            return False

        all_matches.sort(key=lambda x: (x["sourceline"], x["sourcepos"]))

        current_values = [""] * num_selectors
        lines = []

        for entry in all_matches:
            selector_idx = entry["selector_idx"]
            element = entry["element"]

            text = (
                extract_text(
                    element, attributes[selector_idx], recursive_texts[selector_idx]
                )
                .replace("\n", " ")
                .replace(delimiter, " ")
            )

            current_values[selector_idx] = text

            for idx in range(selector_idx + 1, num_selectors):
                current_values[idx] = ""

            if selector_idx == num_selectors - 1:
                lines.append(delimiter.join(current_values) + "\n")

        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"Successfully extracted {len(lines)} rows to: {output_path}")
        return True

    except EnvironmentError:
        return False
    except Exception as e:
        print(f"Processing error: {e}")
        return False
