import pytest
from click.testing import CliRunner
from arkdicts.cli.diff import command


@pytest.fixture
def runner():
    return CliRunner()


def remove_ansi_codes(text):
    import re

    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


@pytest.mark.parametrize(
    "file1_content,file2_content,expected_patterns",
    [
        # 测试用例1: 有差异的情况
        (
            "A\nB\nC",
            "A\nD\nE",
            # 变化：文件头格式改变，符号从 < > 变为 - +
            ["--- old: 1.txt", "+++ new: 2.txt", "- B", "- C", "+ D", "+ E", "@@"],
        ),
        # 测试用例2: 空文件比较
        (
            "",
            "A\nB",
            # 变化：文件头格式改变，符号从 > 变为 +
            ["--- old: 1.txt", "+++ new: 2.txt", "+ A", "+ B"],
        ),
    ],
)
def test_diff(runner, file1_content, file2_content, expected_patterns):
    with runner.isolated_filesystem():
        with open("1.txt", "w", encoding="utf-8") as f:
            f.write(file1_content)
        with open("2.txt", "w", encoding="utf-8") as f:
            f.write(file2_content)
        result = runner.invoke(command, ["1.txt", "2.txt"])

    assert result.exit_code == 0
    clean_output = remove_ansi_codes(result.output)
    for pattern in expected_patterns:
        assert pattern in clean_output, f"Pattern '{pattern}' not found in output"


def test_stat_file_not_exists(runner):
    result = runner.invoke(command, ["nonexistent1.txt", "nonexistent2.txt"])
    assert result.exit_code != 0
    assert "Invalid value" in result.output or "does not exist" in result.output

