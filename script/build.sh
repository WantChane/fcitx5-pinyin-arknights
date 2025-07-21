#!/usr/bin/env bash

set -euo pipefail

shopt -s nullglob

targets=()
process_all=true

while [[ $# -gt 0 ]]; do
    case "$1" in
        --all)
            process_all=true
            shift
            ;;
        *)
            targets+=("$1")
            process_all=false
            shift
            ;;
    esac
done

echo "开始处理..."

./script/clean.sh

if [ "$process_all" = true ]; then
    python script/extend_dictionaries.py --all

    echo "复制所有titles文件..."
    cp -vf input/an_* output/
    cp -vf output/an_* input/

    for py_file in an_*.py; do
        echo "正在执行: ${py_file}"
        mw2fcitx -c "${py_file}"
    done
else
    python script/extend_dictionaries.py "${targets[@]}"

    for target in "${targets[@]}"; do
    
        if [ "$target" = "an_other" ]; then
            echo "复制手动维护的titles文件: ${target}"
            cp -vf "input/${target}_titles.txt" "output/"
        else
            if [ -f "output/${target}_titles.txt" ]; then
                echo "复制自动生成的的titles文件: ${target}"
                cp -vf "output/${target}_titles.txt" "input/"
            else
                echo "警告: output/${target}_titles.txt 不存在"
            fi
        fi

        if [ -f "${target}.py" ]; then
            mw2fcitx -c "${target}.py"
        else
            echo "警告: ${target}.py 不存在"
        fi
    done
fi

echo "所有任务执行完成！"