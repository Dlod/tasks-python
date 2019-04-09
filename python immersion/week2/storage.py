import os
from tempfile import gettempdir
from argparse import ArgumentParser
import json

def load_file(storage_path):
    with open(storage_path, "r") as f:
        return json.load(f)

def add_items(key, val, storage):
    if key in storage:
        tmp_val = storage[key]
        tmp_val.append(val)
    else:
        storage[key] = [val]
    return storage

def clean(storage):
    with open(storage, 'w') as f:
            json.dump({}, f)

def main(args):
    key = args.key
    val = args.val
    clear = args.clear
    storage_path = os.path.join(gettempdir(), 'storage.data')
    if key or val:
        storage = load_file(storage_path) if os.path.exists(storage_path) else {}
    if key and val:
        with open(storage_path, 'w') as f:
            json.dump(add_items(key, val, storage), f)
    elif key and not val:
        if key in storage.keys():
            print(", ".join(storage[key]))
        else:
            print("None")
    elif clear:
        clean(storage_path)   

if __name__ == "__main__":
    parser =  ArgumentParser(description="key:value storage")
    parser.add_argument("--key")
    parser.add_argument("--val")
    parser.add_argument("--clear", action="store_true", default=False)
    main(parser.parse_args())