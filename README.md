# fcitx5-pinyin-prts

使用 [mw2fcitx](https://github.com/outloudvi/mw2fcitx)，制作了 [PRTS](https://prts.wiki/) 的词库。

会在每月 14 日晚八点由 Github Actions 定时更新。

## 词库

| 文件名（前缀）         | 来源                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | 备注                                                                                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| prts_abnormal          | [异常效果](https://prts.wiki/w/%E5%BC%82%E5%B8%B8%E6%95%88%E6%9E%9C)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                |
| prts_activity          | [分类:有活动信息的页面](https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E6%9C%89%E6%B4%BB%E5%8A%A8%E4%BF%A1%E6%81%AF%E7%9A%84%E9%A1%B5%E9%9D%A2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | 包含部分较难过滤的词条, 例如 [良辰迎月](https://prts.wiki/w/%E8%89%AF%E8%BE%B0%E8%BF%8E%E6%9C%88)                                                              |
| prts_activity_v2       | [活动一览](https://prts.wiki/w/%E6%B4%BB%E5%8A%A8%E4%B8%80%E8%A7%88)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | 依赖 PRTS 的分类, 过滤了 [分类:登录活动](https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E7%99%BB%E5%BD%95%E6%B4%BB%E5%8A%A8) 等类型活动                               |
| prts_all               | [特殊:所有页面](https://prts.wiki/w/%E7%89%B9%E6%AE%8A:%E6%89%80%E6%9C%89%E9%A1%B5%E9%9D%A2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | PRTS 的所有词条, 不建议使用                                                                                                                                    |
| prts_branch            | [分支一览](https://prts.wiki/w/%E5%88%86%E6%94%AF%E4%B8%80%E8%A7%88)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                |
| prts_character         | [剧情角色一览](https://prts.wiki/w/%E5%89%A7%E6%83%85%E8%A7%92%E8%89%B2%E4%B8%80%E8%A7%88)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                |
| prts_clothes           | [时装回廊](https://prts.wiki/w/%E6%97%B6%E8%A3%85%E5%9B%9E%E5%BB%8A)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                |
| prts_collection_{1..5} | [刻俄柏的灰蕈迷境/收藏品图鉴](https://prts.wiki/w/%E5%88%BB%E4%BF%84%E6%9F%8F%E7%9A%84%E7%81%B0%E8%95%88%E8%BF%B7%E5%A2%83/%E6%94%B6%E8%97%8F%E5%93%81%E5%9B%BE%E9%89%B4), [傀影与猩红孤钻/长生者宝盒](https://prts.wiki/w/%E5%82%80%E5%BD%B1%E4%B8%8E%E7%8C%A9%E7%BA%A2%E5%AD%A4%E9%92%BB/%E9%95%BF%E7%94%9F%E8%80%85%E5%AE%9D%E7%9B%92), [水月与深蓝之树/生物制品陈设](https://prts.wiki/w/%E6%B0%B4%E6%9C%88%E4%B8%8E%E6%B7%B1%E8%93%9D%E4%B9%8B%E6%A0%91/%E7%94%9F%E7%89%A9%E5%88%B6%E5%93%81%E9%99%88%E8%AE%BE), [探索者的银凇止境/仪式用品索引](https://prts.wiki/w/%E6%8E%A2%E7%B4%A2%E8%80%85%E7%9A%84%E9%93%B6%E5%87%87%E6%AD%A2%E5%A2%83/%E4%BB%AA%E5%BC%8F%E7%94%A8%E5%93%81%E7%B4%A2%E5%BC%95), [萨卡兹的无终奇语/想象实体图鉴](https://prts.wiki/w/%E8%90%A8%E5%8D%A1%E5%85%B9%E7%9A%84%E6%97%A0%E7%BB%88%E5%A5%87%E8%AF%AD/%E6%83%B3%E8%B1%A1%E5%AE%9E%E4%BD%93%E5%9B%BE%E9%89%B4) |                                                                                                                                                                |
| prts_enemy             | [分类:敌人](https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E6%95%8C%E4%BA%BA)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                |
| prts_isw               | [分类:集成战略关卡](https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E9%9B%86%E6%88%90%E6%88%98%E7%95%A5%E5%85%B3%E5%8D%A1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                                                                |
| prts_material          | [分类:材料](https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E6%9D%90%E6%96%99)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                |
| prts_operator          | [分类:干员](https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E5%B9%B2%E5%91%98)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                                                                                                                                                                |
| prts_other             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | 拓展词库，人工维护，需要修改请 [PR](https://github.com/WantChane/fcitx5-pinyin-prts/pulls) 或者 [#1](https://github.com/WantChane/fcitx5-pinyin-prts/issues/1) |
| prts_real_name         | [角色真名](https://prts.wiki/w/%E8%A7%92%E8%89%B2%E7%9C%9F%E5%90%8D)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                |
| prts_term              | [术语释义](https://prts.wiki/w/%E6%9C%AF%E8%AF%AD%E9%87%8A%E4%B9%89)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                |
| prts_terra             | [泰拉词库](https://prts.wiki/w/%E6%B3%B0%E6%8B%89%E8%AF%8D%E5%BA%93)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                |

## 安装

### Weasel

#### 通过 Scoop 自动安装

1. 添加 doge bucket，或者将 [fcitx5-pinyin-prts_rime_dicts.json](https://github.com/WantChane/doge_bucket/blob/master/bucket/fcitx5-pinyin-prts_rime_dicts.json) 添加到您的个人 bucket 中

```shell
scoop bucket add doge https://github.com/WantChane/doge_bucket.git
```

2. 安装 fcitx5-pinyin-prts_rime_dicts

```shell
scoop install fcitx5-pinyin-prts_rime_dicts
```

3. 按需修改您的词库设置，以 rime-ice 为例。

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
# 单一词库生成，以prts_operator为例
mw2fcitx -c prts_operator.py

## 对于来自页面内部数据的词库，需要先执行 script/extend_dictionaries.py，以获取 titles 文件
python script/extend_dictionaries.py
cp -f output/prts_real_name_titles.txt input
mw2fcitx -c prts_real_name.py

# 生成所有词库
./script/build.sh
```
