from pathlib import Path

from tomlkit import TOMLDocument
from tomlkit import parse

from src.utils.directory_utils import find_root

def get_config() -> TOMLDocument:
    root_path = find_root()
    with open(root_path / 'config/config.toml', 'r', encoding='utf-8') as f:
        return parse(f.read())
    
if __name__ == '__main__':
    get_config()