import sys
import time

start_time = time.time()

# N refers to the number of men or women
N = 0

# Preferred is the data of each person and their rankings
preferred = []

# Men is a dictionary of the men and their pairing
men = {}

# Women is a dictionary of the women and their pairing
women = {}

def add_argument(argument=1):
    ''' 
    Checks if the number of arguments is correct 
    '''
    if len(sys.argv) > 2 or len(sys.argv) == 1:
        sys.exit(1)
    else:
        return sys.argv[argument]

def open_file():
    ''' 
    Opens the file and parses the data to return N and the preferred array
    '''
    global N
    file_name = add_argument()
    lines = []
    with open(file_name) as file:
        data = file.readlines()
        for line in data:
            words = line.split()
            lines.append(words)

    N = int(lines[0][0])
    preferred = lines[1:]
    return preferred

def checker():
    '''
    Checks if there are the correct amount of people in the list with N men or women
    '''
    global N
    rows = open_file()
    for row in rows:
        if len(row) == N+1:
            continue
        else:
            sys.exit(1)

    return rows

def checkRankings(preferred):
    '''
    Checks if each person has N people ranked
    '''
    for rank in preferred:
        if len(rank) != N + 1:
            sys.exit(1)

def checkMatch(w, m, m2):
    '''
    Checks whether a women wants her current husband
    or the man that just proposed
    '''
    global preferred
    ladies = preferred[N+1:]

    for rank in ladies:
        if rank[0] == w:
            for man in range(1, N):
                if rank[man] == m2:
                    return True
                elif rank[man] == m:
                    return False
                else:
                    pass

def engage(m, w):
    '''
    Pairs the two together in their respective dictionaries
    '''
    global men
    global women
    men[m] = w
    women[w] = m

def free(m):
    '''
    Sets a husband as a free man
    '''
    global men
    men[m] = 0

def remove(m):
    '''
    Removes an option from a man's ranking
    '''
    global preferred

    preferred[m].pop(1)

def marry(preferred):
    '''
    Implementation of the Gale Shapely Algorithm
    '''

    # Set each person as free in their respective dictionary; 0 means they are not engaged
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
                engaged = women[best]
                if engaged == 0:
                    engage(man, best)
                elif checkMatch(best, engaged, man):
                    engage(man, best)
                    free(engaged)
                    
                else:
                    remove(m)

def listMarriage():
    '''
    Print out the married pairs when marriages are stablized
    '''
    global men
    global women

    for woman, man in women.items():
        print(man, woman)

if __name__ == "__main__":
    '''
    Main function
    '''
    add_argument()
    preferred = checker()
    checkRankings(preferred)
    marry(preferred)
    listMarriage()
    print("--- %s seconds ---" % (time.time() - start_time))
