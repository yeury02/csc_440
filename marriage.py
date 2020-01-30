import sys

N = 0
preferred = []
men = {}
women = {}

def add_argument(argument=1):
    if len(sys.argv) > 2 or len(sys.argv) == 1:
        sys.stdout.write("nothing \n")
        exit(1)
    else:
        return sys.argv[argument]

def open_file():
    global N
    file_name = add_argument()
    lines = []
    with open(file_name) as file:
        data = file.readlines()
        for line in data:
            words = line.split()
            print(words)
            lines.append(words)
    
    N = int(lines[0][0])
    return lines[1:]

def checkRankings(preferred):
    for rank in preferred:
        if len(rank) != N + 1:
            print(len(rank))
            sys.stdout.write("nothing \n")

def checkMatch(w, m, m2):
    global preferred

    for rank in preferred:
        if rank[0] == w:
            if rank[1] == m2:
                return True
            else:
                return False

def engage(m, w):
    global men
    global women
    men[m] = w
    women[w] = m

def free(m):
    global men
    men[m] = 0

def remove(m):
    global preferred

    preferred[m].pop(1)

def marry(preferred):
    # Lets add the woman and men and initialize them as free
    global men
    global women

    for w in range(N, N*2):
        print(preferred[w][0])
        women[preferred[w][0]] = 0

    for m in range(0, N):
        print(preferred[m][0])
        men[preferred[m][0]] = 0

    # Stablize the marriage
    while 0 in (men.values() and women.values()):
        for m in range(0, N):
            man = preferred[m][0]
            best = preferred[m][1]
            if men[man] == 0:
                if best in men.values():
                    remove(m)

                else:
                    engage(man, best)
            else:
                engaged = women[best]
                if checkMatch(best, engaged, man):
                    engage(man, best)
                    free(engaged)
                else:
                    pass               

    print(women)
    print(men)
    return 0

if __name__ == "__main__":
    add_argument()
    preferred = open_file()
    checkRankings(preferred)
    court = marry(preferred)