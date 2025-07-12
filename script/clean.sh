#!/usr/bin/env bash

set -e
shopt -s extglob nullglob

echo "进入目录: input"
cd input || exit

to_delete=( !(fixfile.json|an_other_titles.txt) )

if [ ${#to_delete[@]} -eq 0 ]; then
    echo "在input目录中没有可删除的文件。"
else
    echo "将删除input目录中的以下文件和目录："
    for item in "${to_delete[@]}"; do
        echo "  $item"
    done

    # 删除操作
    rm -rf "${to_delete[@]}"
fi

echo "input目录清理完成。"

echo "进入目录: output"
cd ../output || exit

to_delete=( !(.gitkeep) )

if [ ${#to_delete[@]} -eq 0 ]; then
    echo "在output目录中没有可删除的文件。"
else
    echo "将删除output目录中的以下文件和目录："
    for item in "${to_delete[@]}"; do
        echo "  $item"
    done

    rm -rf "${to_delete[@]}"
fi

echo "output目录清理完成。"