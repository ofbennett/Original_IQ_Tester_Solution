import numpy as np
import copy

"""
By Oscar Bennett, 2018

This code computes all possible solutions the The Original IQ Tester puzzle. In it's current form in picks out all the outcomes with either 8 or 1 pegs left at the end and displays the sequence of moves to reach them.

See here for details of the puzzle and rules:
https://www.amazon.com/Channel-Classic-Challenging-Handcrafted-Original/dp/B001XM3DGM

There are approx 1 million possible sequences in the game when a grid of depth 5 is chosen (as is the case in the wooden puzzle itself)!
"""

class Grid(object):
    def __init__(self,depth,empty_hole):
        self.depth = depth # Size of grid (the wooden game has this = 5)
        self.empty_hole = empty_hole
        self.history = []
        self.finished = False
        self.holes = np.ones((depth,depth))
        for i in range(depth):
            for j in range(depth):
                if i<j:
                    self.holes[i,j] = 2
        self.holes[empty_hole]=0
        Grid.TOTAL_GAMES_FINISHED=0

    def peg_num(self):
        # Counts the pegs remaining in the grid
        k=0
        for i in range(self.depth):
            for j in range(self.depth):
                if i>=j:
                    if self.holes[i,j]==1:
                        k+=1
        return k

    def possible_moves_loc(self,loc):
        # Returns a list of all the possible moves from a given location within the grid
        moves = []
        candidates = [[2,0],[2,2],[0,2],[-2,2],[-2,0],[-2,-2],[0,-2],[2,-2]]

        for can in candidates:
            new_loc = (loc[0]+can[0],loc[1]+can[1])
            if new_loc[0]<0 or new_loc[1]<0:
                continue
            between = (loc[0]+can[0]/2,loc[1]+can[1]/2)
            try:
                if self.holes[new_loc] == 0 and self.holes[between] == 1:
                    moves.append(can)
            except:
                continue

        return moves

    def possible_moves(self):
        # Returns a list of all possible moves in the current state
        moves = {}
        for i in range(self.depth):
            for j in range(self.depth):
                if i>=j:
                    if self.holes[i,j]==1:
                        moves_loc = self.possible_moves_loc((i,j))
                        if moves_loc:
                            moves[(i,j)] = moves_loc
        return moves

    def add_history(self,new_hist):
        self.history.append(new_hist)

    def next_grids(self):
        # Returns all the grid arrangements after each possible move in the current state
        moves = self.possible_moves()
        if not moves:
            self.finished = True
            Grid.TOTAL_GAMES_FINISHED+=1
            return []
        pegs = moves.keys()

        grid_list = []
        for peg in pegs:
            for move in moves[peg]:
                new_grid = copy.deepcopy(grid)
                new_grid.add_history([peg,move])
                new_grid.holes[peg]=0
                new_grid.holes[peg[0]+move[0],peg[1]+move[1]]=1
                new_grid.holes[peg[0]+move[0]/2,peg[1]+move[1]/2]=0
                grid_list.append(new_grid)

        return grid_list

# Define the starting grid setup here
first_grid = Grid(5,(4,1))
print 'Starting grid arrangement:'
print first_grid.holes

n=0
one_count=0
eight_count=0
grid_lineage_next = [first_grid]
while True:
    grid_lineage = grid_lineage_next
    print 'Moves so far: '+ str(n)
    print 'Number of active grids = '+ str(len(grid_lineage))
    print 'Total games finished so far = ' + str(Grid.TOTAL_GAMES_FINISHED)
    grid_lineage_next = []
    for grid in grid_lineage:
        # print grid
        grid_list = grid.next_grids()
        grid_lineage_next += grid_list

    for x in grid_lineage:
        if x.finished == True:
            if x.peg_num() > 7:
                eight_count+=1
                print x.holes
                print 'Final pegs remaining: ' + str(x.peg_num())
                print x.history
            elif x.peg_num() < 2:
                one_count+=1
                if one_count < 21:
                    print x.holes
                    print 'Final pegs remaining: ' + str(x.peg_num())
                    print x.history

    if not grid_lineage_next:
        print 'Total games finished = ' + str(Grid.TOTAL_GAMES_FINISHED)
        print 'Number of one peg games finished  = ' + str(one_count)
        print 'Number of eight peg games finished  = ' + str(eight_count)
        break
    n+=1
