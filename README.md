# fcitx5-pinyin-prts

使用 [mw2fcitx](https://github.com/outloudvi/mw2fcitx)，制作了 [PRTS](https://prts.wiki/) 的词库。

会在每月 14 日晚八点由 Github Actions 定时更新。

## 词库

| 文件名（前缀） | 备注                                   |
| -------------- | -------------------------------------- |
| prts_all       | 全量词库，不建议使用，包含很多奇怪的词 |
| prts_operator  | 干员词库                               |
| prts_enemy     | 敌人词库                               |
| prts_activity  | 活动词库                               |
| prts_material  | 材料词库                               |

| 文件名（后缀） | 备注                 |
| -------------- | -------------------- |
| dict           | fcitx5 词库          |
| dict.yaml      | rime 词库            |
| _titles.txt    | 来自 PRTS 的原始数据 |

## 手动构建

1. 安装依赖。如果遇到了 opencc build 错误，可以尝试使用较早版本的 python，例如 3.10。

```shell
pip install -r requirements.txt
```

2. 如果需要 fcitx-pinyin 字典，需要额外安装 [libime](https://github.com/fcitx/libime)，如果不需要，可以修改 prts.py 中的 generator。你也可以根据 [mw2fcitx](https://github.com/outloudvi/mw2fcitx) ，做出其他修改，有好的点子记得告诉我。😄

```shell
# ubuntu
sudo apt install -y libime-bin

# arch
sudo pacman -S libime
```

3. Run

```shell
# 单一词库生成，例如prts_operator
mw2fcitx -c prts_operator.py

# 生成所有词库
./script/build.sh
```
