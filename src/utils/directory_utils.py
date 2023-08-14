from pathlib import Path

def find_root(root_name='mlops_sp'):
    current_path = Path(__file__).resolve()
    while True:
        parent_path = current_path.parent

        if parent_path.name == root_name:
            return parent_path

        if current_path == parent_path:
            raise Exception(f"找不到{root_name}文件夹")
        current_path = parent_path

if __name__ == "__main__": 
    print(find_root())