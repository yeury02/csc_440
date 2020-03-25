import rubik
from collections import deque
import time

'''
Algorithm Invarient

Definition: 2x2x2 Rubik's Cube, the goal is to make make each side the same color. 
            I accomplished this by using a Breath First Search(BFS) traversal algorithm 
            going two ways. The Start of the cube and the end which are given to us as a
            tuple. Let G=(V,E) where V is the a set of vertices and E is a set of edges (pair of vertices)
            Let start = S and end = E

Initialization (Base Case): I know this base case is working because my program checks if the given S set
                            of points is equal to the E set of points, then the 2x2x2 cube most be solved already.
                            It is technically checking if the moves are in the same order. If cubes are not on the 
                            same state, then I use a two way breath first search algorithm to solve it.

Maintance (Indunction Step) - Assuming there is a path from S to E and they are not on the same state, 
                              start with vertex V
                              list all its neighbors(distance 1)
                              then all their neighbors (distance 2) etc.
                              
                              Algorithm starting at S:
                                   define frontier F
                                   initially = F{s}
                                   repeat F=all neighbors of vertices in F
                                   until all vertices found
                                
                              Algorithm starting at S:
                                   define frontier F
                                   initially = F{e}
                                   repeat F=all neighbors of vertices in F
                                   until all vertices found  
                                
                              as mentioned above, this is a two way searching, I would first make my first move
                              with S and see if there is a path to E, if not then make a move with E and check
                              the same thing over and over.
    
    termination - I know this algorithm terminates correctly because if it finds a path from S to E then it returns
                  that part. However, it keeps checking for paths until it runs out of possible ways to check. If
                  that happens then that means there is not a solution.                   

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