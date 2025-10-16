import re
import pytest
from click.testing import CliRunner
from arkdicts.cli.stat import command


@pytest.fixture
def runner():
    return CliRunner()


def match_table_row(line, char_repr_pattern, unicode_pattern, count):
    pattern = rf"^\s*{char_repr_pattern}\s+{unicode_pattern}\s+{count}\s*$"
    return re.match(pattern, line) is not None


@pytest.mark.parametrize(
    "file_content,expected_matches",
    [
        (
            "Hello, world! How are you?\nI'm fine, thanks.",
            [
                {"char": r"' '", "unicode": r"U\+0020", "count": "6"},
                {"char": r"','", "unicode": r"U\+002C", "count": "2"},
                {"char": r"'\\n'", "unicode": r"U\+000A", "count": "1"},
                {"char": r"'!'", "unicode": r"U\+0021", "count": "1"},
                {"char": r"\"'\"", "unicode": r"U\+0027", "count": "1"},
                {"char": r"'.'", "unicode": r"U\+002E", "count": "1"},
                {"char": r"'\?'", "unicode": r"U\+003F", "count": "1"},
            ],
        ),
        # 测试用例2: 空文件
        (
            "",
            [],
        ),
        # 测试用例3: 只有字母数字，没有特殊字符
        (
            "Hello123World456你好789相沢みなみ",
            [],
        ),
    ],
)
def test_stat(runner, file_content, expected_matches):
    with runner.isolated_filesystem():
        with open("test.txt", "w", encoding="utf-8") as f:
            f.write(file_content)

        result = runner.invoke(command, ["test.txt"])

    assert result.exit_code == 0

    output_lines = result.output.strip().split("\n")

    assert len(output_lines) >= 3, (
        "The output should contain at least a separator line and a table header"
    )

    data_lines = output_lines[3:-1]

    assert len(data_lines) == len(expected_matches), (
        f"The number of data rows does not match. Expected: {len(expected_matches)}, Got: {len(data_lines)}"
    )

    for i, expected_match in enumerate(expected_matches):
        line = data_lines[i]
        assert match_table_row(
            line,
            expected_match["char"],
            expected_match["unicode"],
            expected_match["count"],
        ), f"Line {i + 1} does not match the expected pattern: {expected_match}"


def test_stat_file_not_exists(runner):
    result = runner.invoke(command, ["nonexistent.txt"])
    assert result.exit_code != 0
    assert "Invalid value" in result.output or "does not exist" in result.output
