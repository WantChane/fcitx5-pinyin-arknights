#!/usr/bin/env bash

set -euo pipefail

shopt -s nullglob

echo "开始处理..."

./script/clean.sh

python script/extend_dictionaries.py

cp -vf input/prts_* output/
cp -vf output/prts_* input/

for py_file in prts_*.py; do
    echo "正在处理: ${py_file}"
    mw2fcitx -c "${py_file}"
done

echo "所有文件处理完成！"