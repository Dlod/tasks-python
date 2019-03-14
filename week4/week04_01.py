import tempfile, os

class File:

    def __init__(self, file, content=None):
        self.file = file
        if content:
            self.open_file = open(self.file, 'w')
            self.write(content)
        self.open_file = open(self.file, 'r+')

    def __iter__(self):
        return self.open_file

    def get_content(self):
        return self.open_file.read()

    def __del__(self):
        self.open_file.close()
        del self.open_file

    def write(self, line):
        self.open_file.write(line)

    def __add__(self, obj):
        new_file = File(file=os.path.join(tempfile.gettempdir(), "new_file"),
        content=self.get_content()+obj.get_content())
        return new_file

    def __str__(self):
        return self.file
