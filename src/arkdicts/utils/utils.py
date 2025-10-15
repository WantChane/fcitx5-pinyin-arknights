from arkdicts.constant import OUTPUT_DIR


def generate_filepath(dict_name: str) -> tuple[str, str, str]:
    titles_path = f"{OUTPUT_DIR}/titles/{dict_name}_titles.txt"
    rime_path = f"{OUTPUT_DIR}/rime_dicts/{dict_name}.dict.yaml"
    fcitx_path = f"{OUTPUT_DIR}/fcitx5_dicts/{dict_name}.dict"
    return titles_path, rime_path, fcitx_path
