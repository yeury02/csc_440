import sys


try:
    file_name = sys.argv[1]
    with open(file_name) as file:
        data = file.readlines()
        for line in data:
            words = line.split()
            print(words)
            #if len(line.split) ==
except:
    sys.stdout.write("nothing")
    exit(1)