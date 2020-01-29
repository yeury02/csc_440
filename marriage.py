import sys

#print(sys.argv)
try:
    file_name = sys.argv[1]
    with open(file_name) as file:
        data = file.read()
        print(data)
except:
    sys.stdout.write("nothing")
    exit(1)