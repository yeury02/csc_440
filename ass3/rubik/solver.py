import rubik
from collections import deque
import time

'''
Algorithm Invarient

Definition: 

'''
def shortest_path(start, end):

    """
      Using 2-way BFS, finds the shortest path from start_position to
      end_position. Returns a list of moves.

      You can use the rubik.quarter_twists move set.
      Each move can be applied using rubik.perm_apply
    """

    start_time = time.time()
    frontier = deque()
    frontier.append(start)
    parent = {start: None}

    answer_found = False
    while frontier:
        current_twist = frontier.popleft()
        if current_twist == end:
            answer_found = True
            break

        for i in range(6):
            tmp = rubik.perm_apply(rubik.quarter_twists[i], current_twist)

            if tmp not in parent:
                if i % 2 == 0:
                    parent[tmp] = i + 1
                else:
                    parent[tmp] = i - 1
                frontier.append(tmp)

    answer = deque()
    if answer_found:
        moves = end
        j = parent[moves]
        while parent[moves] is not None:
            if j % 2 == 0:
                answer.appendleft(rubik.quarter_twists[j+1])
            else:
                answer.appendleft(rubik.quarter_twists[j - 1])
            moves = rubik.perm_apply(rubik.quarter_twists[j], moves)
            j = parent[moves]
        #print("\n--- %s seconds ---" % (time.time() - start_time))
        return list(answer)
    else:
        #print("\n--- %s seconds ---" % (time.time() - start_time))
        return None