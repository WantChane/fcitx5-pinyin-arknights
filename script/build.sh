#!/usr/bin/env bash

set -euo pipefail

shopt -s nullglob

echo "开始处理..."

python script/prts_operator_extend.py

cp input/prts_operator_extend_titles.txt output/prts_operator_extend_titles.txt -f

for py_file in prts_*.py; do
    echo "正在处理: ${py_file}"
    mw2fcitx -c "${py_file}"
done

echo "所有文件处理完成！"