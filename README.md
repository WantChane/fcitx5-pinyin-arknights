# fcitx5-pinyin-prts

使用 [mw2fcitx](https://github.com/outloudvi/mw2fcitx)，制作了 [PRTS](https://prts.wiki/) 的词库。

会在每月 14 日晚八点由 Github Actions 定时更新。

## 词库

| 文件名（前缀）       | 备注                                   |
| -------------------- | -------------------------------------- |
| prts_activity        | 活动词库                               |
| prts_all             | 全量词库，不建议使用，包含很多奇怪的词 |
| prts_enemy           | 敌人词库                               |
| prts_material        | 材料词库                               |
| prts_operator        | 干员词库                               |
| prts_operator_extend | 干员真名词库                               |

| 文件名（后缀） | 备注                 |
| -------------- | -------------------- |
| dict           | fcitx5 词库          |
| dict.yaml      | rime 词库            |
| _titles.txt    | 来自 PRTS 的原始数据 |

## 安装

### Weasel

#### 通过 Scoop 自动安装

1. 添加 doge bucket，或者将 [fcitx5-pinyin-prts_all_dicts.json](https://github.com/WantChane/doge_bucket/blob/master/bucket/fcitx5-pinyin-prts_all_dicts.json) 复制到您的个人 bucket 中

```shell
scoop bucket add doge https://github.com/WantChane/doge_bucket.git
```

2. 安装 fcitx5-pinyin-prts_all_dicts

```shell
scoop install fcitx5-pinyin-prts_all_dicts
```

3. 修改您的词库设置，以 rime-ice 为例，

```yaml
# rime_ice.dict.yaml
---
name: rime_ice
version: "2024-11-27"
import_tables:
  - cn_dicts/8105     # 字表
  # - cn_dicts/41448  # 大字表（按需启用）（启用时和 8105 同时启用并放在 8105 下面）
  - cn_dicts/base     # 基础词库
  - cn_dicts/ext      # 扩展词库
  - cn_dicts/tencent  # 腾讯词向量（大词库，部署时间较长）
  - cn_dicts/others   # 一些杂项
  
  # 建议把扩展词库放到下面，有重复词条时，最上面的权重生效
  # - mydict1           # 挂载配置目录下的 mydict1.dict.yaml 词库文件
  # - cn_dicts/mydict2  # 挂载 cn_dicts 目录里的 mydict2.dict.yaml 词库文件
- cn_dicts/prts_operator
- cn_dicts/prts_activity
...
```

4. 更新

```shell
scoop update fcitx5-pinyin-prts_all_dicts
```

### 其他发行版

暂时没有，以后再说

## 手动构建

1. 安装依赖。如果遇到了 opencc build 错误，可以尝试使用较早版本的 python，例如 3.10。

```shell
pip install -r requirements.txt
```

1. 如果需要 fcitx 字典，需要额外安装 [libime](https://github.com/fcitx/libime)，如果不需要，可以修改配置中的 generator。你也可以根据 [mw2fcitx](https://github.com/outloudvi/mw2fcitx) ，做出其他修改，有好的点子记得告诉我。😄

```shell
# ubuntu
sudo apt install -y libime-bin

# arch
sudo pacman -S libime
```

3. Run

```shell
# 单一词库生成，以operator为例
mw2fcitx -c prts_operator.py

# 生成所有词库
./script/build.sh
```
