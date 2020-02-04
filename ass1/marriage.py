import sys

N = 0
preferred = []
men = {}
women = {}

def add_argument(argument=1):
    if len(sys.argv) > 2 or len(sys.argv) == 1:
        sys.stdout.write("nothing \n")
        sys.exit(1)
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
            lines.append(words)

    N = int(lines[0][0])
    preferred = lines[N+1:(N*2)+1] + lines[1:N+1]
    return preferred

def checker():
    global N
    rows = open_file()
    for row in rows:
        if len(row) == N+1:
            continue
        else:
            sys.stdout.write('nothing \n')
            sys.exit(1)

    return rows

def checkRankings(preferred):
    for rank in preferred:
        if len(rank) != N + 1:
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
        women[preferred[w][0]] = 0

    for m in range(0, N):
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

def listMarriage():
    global men
    global women

    for woman, man in women.items():
        print(woman, man)

if __name__ == "__main__":
    add_argument()
    preferred = checker()
    checkRankings(preferred)
    marry(preferred)
    listMarriage()