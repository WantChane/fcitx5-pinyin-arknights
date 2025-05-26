# fcitx5-pinyin-prts

使用 [mw2fcitx](https://github.com/outloudvi/mw2fcitx)，制作了 [PRTS](https://prts.wiki/) 的词库。

会在每月 14 日晚八点由 Github Actions 定时更新。

## 词库

| 文件名（前缀） | 来源                                                                                                                                     |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| prts_activity  | [分类:有活动信息的页面](https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E6%9C%89%E6%B4%BB%E5%8A%A8%E4%BF%A1%E6%81%AF%E7%9A%84%E9%A1%B5%E9%9D%A2) |
| prts_all       | 全量词库，不建议使用，包含很多奇怪的词                                                                                                   |
| prts_character | [剧情角色一览](https://prts.wiki/w/%E5%89%A7%E6%83%85%E8%A7%92%E8%89%B2%E4%B8%80%E8%A7%88)                                               |
| prts_enemy     | [分类:敌人](https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E6%95%8C%E4%BA%BA)                                                                   |
| prts_material  | [分类:材料](https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E6%9D%90%E6%96%99)                                                                   |
| prts_operator  | [分类:干员](https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E5%B9%B2%E5%91%98)                                                                   |
| prts_real_name | [角色真名](https://prts.wiki/w/%E8%A7%92%E8%89%B2%E7%9C%9F%E5%90%8D)                                                                     |
| prts_terra     | [泰拉词库](https://prts.wiki/w/%E6%B3%B0%E6%8B%89%E8%AF%8D%E5%BA%93)                                                                     |

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

2. 如果需要 fcitx 字典，需要额外安装 [libime](https://github.com/fcitx/libime)，如果不需要，可以修改配置中的 generator。你也可以根据 [mw2fcitx](https://github.com/outloudvi/mw2fcitx) ，做出其他修改，有好的点子记得告诉我。😄

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
