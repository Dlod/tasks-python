import sys
import argparse


class FileReader():
    """Класс FileReader помогает читать из файла"""
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def read(self):
        try:
            with open(self.path_to_file, "r") as f:
                return f.read()
        except IOError as err:
            return ""
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser("filereader")
    parser.add_argument("path_to_file", type=str, help="Путь до файла который надо прочитать")
    reader = FileReader(parser.parse_args().path_to_file)
    print(reader.read())