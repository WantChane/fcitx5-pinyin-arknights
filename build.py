#!/bin/env python

import argparse
import os
import shutil
from script.extend_dictionaries import parse_page, parse_sequential_page
from constant import ALL_DICTS, CLEAN_EXCLUDE_FILES, MANUAL_DICTS, REQUEST_DELAY
from mw2fcitx.main import inner_main


PAGES = {
    "an_collection_1": {
        "function": parse_page,
        "args": ["刻俄柏的灰蕈迷境/收藏品图鉴", "output/an_collection_1_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_collection_2": {
        "function": parse_page,
        "args": ["傀影与猩红孤钻/长生者宝盒", "output/an_collection_2_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_collection_3": {
        "function": parse_page,
        "args": ["水月与深蓝之树/生物制品陈设", "output/an_collection_3_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_collection_4": {
        "function": parse_page,
        "args": ["探索者的银凇止境/仪式用品索引", "output/an_collection_4_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_collection_5": {
        "function": parse_page,
        "args": ["萨卡兹的无终奇语/想象实体图鉴", "output/an_collection_5_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_collection_6": {
        "function": parse_page,
        "args": ["岁的界园志异/珍玩集册", "output/an_collection_6_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr:first-child>th:nth-child(2)"
        },
    },
    "an_character": {
        "function": parse_page,
        "args": ["剧情角色一览", "output/an_character_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr>td:first-child",
            "recursive_text": True,
        },
    },
    "an_real_name": {
        "function": parse_sequential_page,
        "args": ["角色真名", "output/an_real_name_titles.txt"],
        "kwargs": {
            "selectors": [
                "div>table.wikitable>tbody>tr>td:nth-child(2)",
                "div>table.wikitable>tbody>tr>td:nth-child(3)",
            ],
            "recursive_texts": [True, True],
        },
    },
    "an_terra": {
        "function": parse_page,
        "args": ["泰拉词库", "output/an_terra_titles.txt"],
        "kwargs": {
            "selector": "div>table.wikitable>tbody>tr>td:first-child",
            "recursive_text": True,
        },
    },
    "an_clothes": {
        "function": parse_page,
        "args": ["时装回廊", "output/an_clothes_titles.txt"],
        "kwargs": {"selector": ".charnameEn"},
    },
    "an_branch": {
        "function": parse_page,
        "args": ["分支一览", "output/an_branch_titles.txt"],
        "kwargs": {"selector": "font>strong"},
    },
    "an_activity_v2": {
        "function": parse_sequential_page,
        "args": ["活动一览", "output/an_activity_v2_titles.txt"],
        "kwargs": {
            "selectors": [
                "div>table.wikitable>tbody>tr>td:nth-child(2)>a",
                "div>table.wikitable>tbody>tr>td:nth-child(3)",
            ],
            "recursive_texts": [True, True],
        },
    },
    "an_term": {
        "function": parse_page,
        "args": ["术语释义", "output/an_term_titles.txt"],
        "kwargs": {"selector": "h2~p>b>span"},
    },
    "an_abnormal": {
        "function": parse_page,
        "args": ["异常效果", "output/an_abnormal_titles.txt"],
        "kwargs": {"selector": "div>table>tbody>tr>td:nth-child(3)"},
    },
    "an_summons": {
        "function": parse_page,
        "args": ["召唤物一览", "output/an_summons_titles.txt"],
        "kwargs": {"selector": "div>table>tbody>tr>td>a"},
    },
}


def clean_folders(exclude_files=CLEAN_EXCLUDE_FILES):
    if exclude_files is None:
        exclude_files = []
    elif isinstance(exclude_files, str):
        exclude_files = [exclude_files]

    for folder in ["input", "output"]:
        folder_path = os.path.abspath(folder)
        if not os.path.exists(folder_path):
            print(f"{folder_path} does not exist")
            continue

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            rel_path = os.path.join(folder, item)
            if rel_path in exclude_files or item_path in exclude_files:
                print(f"\tSkip delete: {rel_path}")
                continue
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                    print(f"\tDelete file: {rel_path}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"\tDelete dir: {rel_path}")
            except Exception as e:
                print(f"\tDelete {rel_path} failed: {str(e)}")


def copy_titles(target, reverse_list=MANUAL_DICTS):

    output_file = os.path.join("output", f"{target}_titles.txt")
    input_file = os.path.join("input", f"{target}_titles.txt")

    if target in reverse_list:
        source = input_file
        destination = output_file
        direction = "input → output"
    else:
        source = output_file
        destination = input_file
        direction = "output → input"

    os.makedirs(os.path.dirname(destination), exist_ok=True)

    try:
        shutil.copy2(source, destination)
        print(f"Copied {direction}: {destination}")
    except FileNotFoundError:
        print(f"Source file not found: {source}")
    except Exception as e:
        print(f"Copy failed: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Build dictionaries")
    parser.add_argument(
        "-d",
        "--dictionary",
        help="Comma-separated dictionary names to build (must exist in ALL_DICTS)",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        default=False,
        help="Build all dictionaries in ALL_DICTS",
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        default=False,
        help="Clean input/output directories",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        default=False,
        help="List all available dictionaries and exit",
    )
    args = parser.parse_args()

    if not set(PAGES.keys()).issubset(ALL_DICTS):
        invalid_tasks = set(PAGES.keys()) - ALL_DICTS
        parser.error(
            f"PAGES contains dictionaries not in ALL_DICTS: {', '.join(invalid_tasks)}\n"
            f"Valid names: {', '.join(ALL_DICTS)}"
        )

    if args.list:
        print("Available dictionaries:")
        for i, name in enumerate(sorted(ALL_DICTS), 1):
            print(f"{i:>2}. {name}")
        return

    conflicts = []
    if args.all and args.dictionary:
        conflicts.append("--all and --dictionary")
    if conflicts:
        parser.error(f"Cannot use simultaneously: {', '.join(conflicts)}")

    if not any([args.dictionary, args.all, args.clean]):
        print("No action requested. Use -h for help.")
        return

    if args.clean:
        print("Cleaning directories...")
        clean_folders()
        print("Cleaning completed")

    dicts = set()
    if args.all:
        dicts = ALL_DICTS
    elif args.dictionary:
        names = args.dictionary.split(",")
        dicts.update(name.strip() for name in names)

    invalid_dicts = dicts - ALL_DICTS
    if invalid_dicts:
        parser.error(
            f"Invalid dictionaries: {', '.join(invalid_dicts)}\n"
            f"Valid options: {', '.join(ALL_DICTS)}"
        )

    request_args = {"request_delay": REQUEST_DELAY}
    for d in dicts:
        print(f"{'='*50}")
        if d in PAGES:
            print(f"Generating titles file for {d}...")
            page = PAGES[d]
            page["function"](*page["args"], **page["kwargs"], **request_args)
        print(f"Building dictionary: {d}")
        copy_titles(d)
        try:
            inner_main(["-c", f"conf/{d}.py"])
            print(f"Successfully built {d}")
        except Exception as e:
            print(f"Failed to build {d}: {str(e)}")
        print(f"{'='*50}")


if __name__ == "__main__":
    main()
