import re
from typing import List
import regex


def tweak_trim_parentheses_suffix():
    """生成去除字符串末尾括号及内容"""

    def cb(items: List[str]) -> List[str]:
        pattern = re.compile(r"\s*[（(][^（）)]*[）)]$")
        return [pattern.sub("", item) for item in items]

    return cb


import regex
from typing import List

from typing import List


def tweak_remove_regex_anywhere(regexes):
    from re import compile as regex_compile

    combined_pattern = r"(?:%s)" % "|".join(f"(?:{r})" for r in regexes)
    compiled = regex_compile(combined_pattern)

    def cb(items: List[str]):
        return [s for s in items if not compiled.search(s)]

    return cb


def tweak_remove_pure_chinese():
    """生成去除列表中纯汉字的项（保留含非汉字的项）"""

    def cb(items: List[str]) -> List[str]:
        pattern = regex.compile(r"^\p{Han}+$", regex.UNICODE)
        return [item for item in items if not pattern.fullmatch(item)]

    return cb
