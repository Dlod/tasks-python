import tempfile, os, uuid

class File:

    def __init__(self, file):
        self.file = file
        self.position = 0
        if not os.path.exists(self.file):
            open(self.file, 'w').close()

    def write(self, content):
        with open(self.file, "w") as f:
            f.write(content)

    def read(self):
        with open(self.file, 'r') as f:
            return f.read()

    def __add__(self, obj):
        new_path = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
        new_file = type(self)(new_path)
        new_file.write(self.read() + obj.read())
        return new_file

    def __str__(self):
        return self.file

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.file, 'r') as f:
            f.seek(self.position)
            line = f.readline()
            if not line:
                self.position = 0
                raise StopIteration('EOF')
            self.position = f.tell()
            return line
