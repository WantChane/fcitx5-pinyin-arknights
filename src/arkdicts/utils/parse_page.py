import re
import os
import time
import urllib.parse
from bs4.element import NavigableString
import requests
from bs4 import BeautifulSoup, CData, Comment, Tag
from typing import Callable, Dict, List, Optional
from arkdicts.constant import USER_AGENT, REQUEST_DELAY

SEMANTIC_SKIP_TAGS = {
    "del",
    "script",
    "style",
}
SEMANTIC_BLOCK_TAGS = {
    "div",
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ul",
    "ol",
    "li",
    "table",
    "tr",
    "section",
    "article",
}
SEMANTIC_INLINE_TAGS = {
    "b",
    "strong",
    "i",
    "em",
    "u",
    "span",
    "a",
    "code",
}
SEMANTIC_BREAK_TAGS = {
    "br",
}


def fetch_page_content(
    page_title: str,
    base_url: str = "https://prts.wiki/api.php",
    request_delay: int = REQUEST_DELAY,
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


def extract_text(
    attribute: Optional[str] = None, recursive: bool = True
) -> Callable[[Tag], str]:
    def extract_text_inner(element: Tag) -> str:
        if attribute:
            return element.get(attribute, "").strip()  # pyright: ignore[reportAttributeAccessIssue,reportOptionalMemberAccess]
        return (
            element.get_text(strip=True)
            if recursive
            else "".join(element.find_all(string=True, recursive=False)).strip()
        )

    return extract_text_inner


DEFAULT_EXTRACTOR = extract_text()


def semantic_extract_text(
    skip_tags: set = SEMANTIC_SKIP_TAGS,
    block_tags: set = SEMANTIC_BLOCK_TAGS,
    inline_tags: set = SEMANTIC_INLINE_TAGS,
    break_tags: set = SEMANTIC_BREAK_TAGS,
    block_separator: str = "|",
) -> Callable[[Tag], str]:
    def semantic_extract_text_inner(element: Tag) -> str:
        parts = []
        for child in element.children:
            if isinstance(child, (Comment, CData)):
                continue
            if isinstance(child, NavigableString):
                parts.append(child.strip(" "))
                continue

            if child.name in skip_tags:  # pyright: ignore[reportAttributeAccessIssue]
                continue
            if child.name in break_tags:  # type: ignore[attr-defined]
                parts.append(block_separator)
                continue
            if child.name in block_tags:  # pyright: ignore[reportAttributeAccessIssue]
                content = semantic_extract_text_inner(child)  # pyright: ignore[reportArgumentType]
                if content:
                    parts.append(content)
                    parts.append(block_separator)
            elif child.name in inline_tags:  # pyright: ignore[reportAttributeAccessIssue]
                parts.append(child.get_text(strip=True, separator=""))
            else:
                parts.append(semantic_extract_text_inner(child))  # pyright: ignore[reportArgumentType]
        result = "".join(parts)

        return re.sub(r"\|+", "|", result).strip(block_separator + " ")

    return semantic_extract_text_inner


def parse_page(
    page_title: str,
    output_path: str,
    selector: str,
    extractor: Callable[[Tag], str] = DEFAULT_EXTRACTOR,
) -> bool:
    """提取页面数据"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        soup = fetch_page_content(page_title)
        elements = soup.select(selector)

        if not elements:
            print(f"No elements found matching selector '{selector}'")
            return False

        texts = [extractor(el) + "\n" for el in elements]

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
    extractor: Optional[List[Callable[[Tag], str]]] = None,
    delimiter: str = ",",
) -> bool:
    """提取结构化页面数据"""
    if len(selectors) != 1:
        raise ValueError(
            "Selectors must contain and only contain a set of root node selectors"
        )

    root_selector, child_selectors = next(iter(selectors.items()))

    num_selectors = len(child_selectors)

    if extractor is None:
        extractor = [DEFAULT_EXTRACTOR] * num_selectors

    if len(extractor) != num_selectors:
        raise ValueError("Extractor count must match the number of child selectors")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        soup = fetch_page_content(page_title)
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
                    extractor[i](elements[0]).replace("\n", " ").replace(delimiter, " ")
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
    extractor: Optional[List[Callable[[Tag], str]]] = None,
    delimiter: str = ",",
) -> bool:
    num_selectors = len(selectors)

    if extractor is None:
        extractor = [DEFAULT_EXTRACTOR] * num_selectors

    if len(extractor) != num_selectors:
        raise ValueError("Extractor count must match the number of selectors")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        soup = fetch_page_content(page_title)

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
                extractor[selector_idx](element)
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
