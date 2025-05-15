# fcitx5-pinyin-prts

使用 [mw2fcitx](https://github.com/outloudvi/mw2fcitx)，制作了 [PRTS](https://prts.wiki/) 的词库。

没有针对 PRTS 定制 tweaks，暂时没有思路。

会在每月 14 日晚八点由 Github Actions 定时更新。

## 手动构建

1. 安装依赖，也就是 mw2fcitx。如果遇到了 opencc build 错误，可以尝试使用较早版本的 python，例如 3.10

```shell
pip install -r requirements.txt
```

2. 如果需要 fcitx-pinyin 字典，需要额外安装 libime，如果不需要，可以修改 prts.py 中的 generator。你也可以根据 [mw2fcitx](https://github.com/outloudvi/mw2fcitx) ，做出其他修改，有好的点子记得告诉我。😄

```shell
# ubuntu
sudo apt install -y libime-bin

# arch
sudo pacman -S libime
```

3. Run

```shell
mw2fcitx -c prts.py
```
