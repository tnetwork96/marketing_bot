import os.path


class FileHandler(object):

    @staticmethod
    def read_file(file_name):
        try:
            with open(file_name, "r") as f:
                data = f.read().strip()
        except FileNotFoundError:
            data = ""
            print(f"{file_name} not exist")
        return data

    @staticmethod
    def write_file(file_name, string, override=False):
        if not override:
            with open(file_name, "a") as f:
                f.write(string + "\n")
        else:
            with open(file_name, "w") as f:
                f.write(string)
