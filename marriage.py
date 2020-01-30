import sys

#len(men) and len(women)
N = 0
file_rows = []

#men = {}
#women = {}

def addArgument(argument=1):
    if len(sys.argv) > 2 or len(sys.argv) == 1:
        sys.stdout.write("nothing")
        sys.exit(1)
    else:
        return sys.argv[argument]

def openFile():
    global N
    file_name = addArgument()
    with open(file_name) as file:
        data = file.readlines()
        N = int(data[0])
        for line in data:
            words = line.split()
            file_rows.append(words)
        file_rows.pop(0)
        return file_rows

def checker():
    global N
    rows = openFile()
    for row in rows:
        if len(row) == N+1:
            continue
        else:
            sys.stdout.write('nothing')
            sys.exit(1)
    # print(i)

if __name__ == "__main__":
    addArgument()
    #openFile()
    checker()