from pathlib import Path

from tomlkit import TOMLDocument
from tomlkit import parse

from src.utils.decorater import chdir_to_project_root, use_log

@use_log
# @chdir_to_project_root
def get_config(file: Path | str) -> TOMLDocument:
    with open('config.toml', 'r', encoding='utf-8') as f:
        print(parse(f.read()))
        return parse(f.read())
    
if __name__ == '__main__':
    get_config()