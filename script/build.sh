#!/usr/bin/env bash

set -euo pipefail

shopt -s nullglob

source ./script/log.sh

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

info "开始处理..."

./script/clean.sh

if [ "$process_all" = true ]; then
    python script/extend_dictionaries.py --all

    info "复制所有titles文件..."
    cp -vf input/an_* output/
    cp -vf output/an_* input/

    for py_file in an_*.py; do
        info "正在执行: ${py_file}"
        mw2fcitx -c "${py_file}"
    done
else
    python script/extend_dictionaries.py "${targets[@]}"

    for target in "${targets[@]}"; do
    
        if [ "$target" = "an_other" ]; then
            info "复制手动维护的titles文件: ${target}"
            cp -vf "input/${target}_titles.txt" "output/"
        else
            if [ -f "output/${target}_titles.txt" ]; then
                info "复制自动生成的的titles文件: ${target}"
                cp -vf "output/${target}_titles.txt" "input/"
            else
                warn "output/${target}_titles.txt 不存在"
            fi
        fi

        if [ -f "${target}.py" ]; then
            info "正在执行: ${target}.py"
            mw2fcitx -c "${target}.py"
        else
            warn "${target}.py 不存在"
        fi
    done
fi

success "所有任务执行完成！"