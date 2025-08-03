import sys
import os
import random
import string

def random_name(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_random_file(path, size_kb=1):
    with open(path, 'wb') as f:
        f.write(os.urandom(size_kb * 1024))

def generate_fs(base_path, depth=3, max_dirs=3, max_files=5):
    if depth == 0:
        return

    os.makedirs(base_path, exist_ok=True)

    # Create random files
    for _ in range(random.randint(1, max_files)):
        file_name = random_name() + ".txt"
        file_path = os.path.join(base_path, file_name)
        create_random_file(file_path, size_kb=random.randint(1, 5))

    # Create subdirectories
    for _ in range(random.randint(1, max_dirs)):
        dir_name = random_name()
        dir_path = os.path.join(base_path, dir_name)
        generate_fs(dir_path, depth - 1, max_dirs, max_files)

if __name__ == "__main__":
    root = "./playground"
    if len(sys.argv) > 1:
        root = f"./{sys.argv[1]}"
    if not os.path.exists(root):
        os.mkdir(root)

    generate_fs(root, depth=4, max_dirs=4, max_files=6)
    print(f"Random file structure generated under {root}")
