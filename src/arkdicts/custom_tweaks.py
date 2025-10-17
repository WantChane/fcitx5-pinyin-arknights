import re
from typing import List


def tweak_trim_parentheses_suffix():
    def trim_parentheses_suffix(items: List[str]) -> List[str]:
        pattern = re.compile(r"\s*[（(][^（）)]*[）)]$")
        return [pattern.sub("", item) for item in items]

    return trim_parentheses_suffix


def tweak_delete_by_regex(regexes):
    from re import compile as regex_compile

    combined_pattern = r"(?:%s)" % "|".join(f"(?:{r})" for r in regexes)
    compiled = regex_compile(combined_pattern)

    def delete_by_regex(items: List[str]):
        return [s for s in items if not compiled.search(s)]

    return delete_by_regex


def tweak_replace_regex(regex_pattern: str):
    pattern = re.compile(regex_pattern)

    def cb(items: List[str]) -> List[str]:
        ret = []
        for item in items:
            modified_item = pattern.sub("", item)
            ret.append(modified_item)
        return ret

    return cb


def tweak_find_chinese(allowed_chars=None):
    if allowed_chars is None:
        allowed_chars = []
    allowed = re.escape("".join(allowed_chars))
    pattern = re.compile(
        f"([\\u4e00-\\u9fff{allowed}]+)|([^\\u4e00-\\u9fff{allowed}]+)"
    )

    def find_chinese(items: List[str]) -> List[str]:
        result = []
        for item in items:
            parts = []
            for match in pattern.finditer(item):
                chinese_part = match.group(1)
                non_chinese_part = match.group(2)
                if chinese_part:
                    parts.append(chinese_part)
                else:
                    parts.append(non_chinese_part)
            filtered = [p for p in parts if p]
            result.extend(filtered)
        return result

    return find_chinese


def tweak_remove_chars(chars):
    has_multi_char = any(len(char) > 1 for char in chars)

    if has_multi_char:
        print("Wanning: tweak_remove_chars is intended for single characters only.")

    trans_table = str.maketrans("", "", "".join(chars))

    def remove_chars(words):
        return [word.translate(trans_table) for word in words]

    return remove_chars


def tweak_mapping(mapping_dict):
    def mapping(words):
        result = []
        append = result.append

        for word in words:
            if word in mapping_dict:
                new_val = mapping_dict[word]
                if new_val is None:
                    continue
                elif isinstance(new_val, list):
                    result.extend(new_val)
                elif isinstance(new_val, str):
                    result.append(new_val)
            else:
                append(word)

        return result

    return mapping


def tweak_ignore_comments():
    def ignore_comments(words):
        return [word for word in words if not word.startswith("#")]

    return ignore_comments
