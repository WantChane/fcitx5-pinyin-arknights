#!/usr/bin/env bash

shopt -s nullglob

source ./script/log.sh

remote_labels=$(gh label list --json name -q '.[].name' --limit 100 | grep '^incremental: ')

local_labels=()
for file in an_*.py; do
    dict_name="${file%.py}"
    label_name="incremental: $dict_name"
    local_labels+=("$label_name")
done

to_delete=()
while IFS= read -r rlabel; do
    if ! printf '%s\n' "${local_labels[@]}" | grep -qxF "$rlabel"; then
        to_delete+=("$rlabel")
    fi
done <<< "$remote_labels"

to_create=()
for llabel in "${local_labels[@]}"; do
    if ! grep -qxF "$llabel" <<< "$remote_labels"; then
        to_create+=("$llabel")
    fi
done

if [ ${#to_delete[@]} -gt 0 ]; then
    info "删除 ${#to_delete[@]} 个旧标签..."
    for label in "${to_delete[@]}"; do
        gh label delete "$label" --yes
        warn "已删除: '$label'"
    done
fi

if [ ${#to_create[@]} -gt 0 ]; then
    info "创建 ${#to_create[@]} 个新标签..."
    for label in "${to_create[@]}"; do
        lib_name="${label#incremental: }"
        gh label create "$label" --color "#1BA784" --description "增量更新词库: $lib_name"
        info "已创建: '$label'"
    done
fi

success "标签同步完成！保留标签: ${#local_labels[@]}个 | 删除: ${#to_delete[@]}个 | 新增: ${#to_create[@]}个"