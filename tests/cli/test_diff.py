import pytest
from click.testing import CliRunner
from arkdicts.cli.diff import command


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.parametrize(
    "file1_content,file2_content,expected_patterns",
    [
        # 测试用例1: 有差异的情况
        (
            "A\nB\nC",
            "A\nD\nE",
            ["--- 1.txt", "+++ 2.txt", "< B", "< C", "> D", "> E", "---"],
        ),
        # 测试用例2: 完全相同的文件
        (
            "A\nB\nC",
            "A\nB\nC",
            ["--- 1.txt", "+++ 2.txt"],
        ),
        # 测试用例3: 空文件比较
        ("", "A\nB", ["--- 1.txt", "+++ 2.txt", "> A", "> B"]),
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
    for pattern in expected_patterns:
        assert pattern in result.output, f"Pattern '{pattern}' not found in output"


def test_stat_file_not_exists(runner):
    result = runner.invoke(command, ["nonexistent1.txt", "nonexistent2.txt"])
    assert result.exit_code != 0
    assert "Invalid value" in result.output or "does not exist" in result.output
