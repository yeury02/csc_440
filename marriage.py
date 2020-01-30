import sys

def add_argument(argument=1):
    if len(sys.argv) > 2 or len(sys.argv) == 1:
        sys.stdout.write("nothing")
        sys.exit(1)
    else:
        return sys.argv[argument]

def open_file():
    file_name = add_argument()
    with open(file_name) as file:
        data = file.readlines()
        for line in data:
            words = line.split()

        size = data[0]
        print(size)
        return print(words[1:])
if __name__ == "__main__":
    add_argument()
    open_file()