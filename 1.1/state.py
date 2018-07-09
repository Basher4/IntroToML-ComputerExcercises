def printline(l, i):
    print('{}|{}|{}'.format(l[i+0], l[i+1], l[i+2]))

class State:
    def __init__(self, tileValues):
        """
        Indecies of tiles:
            0 | 1 | 2
            3 | 4 | 5
            6 | 7 | 8
        
        If 1 has index 0 in list -> 1 is in UL corner
        0 is gap

        self.values = [1,2,3,4,0,5,6,7,8]
        """

        self.values = tileValues
    
    # assigns score to the current state self compared to the finalState
    def evaluation_function(self, finalState):
        #return self._tile_distance_ef(finalState)
        return self._distance_difference(finalState)

    # calculates distance of  tile from its final position
    def _tile_distance_ef(self, finalState):
        def get_distance_of_two_tiles(_a, _b):
            ax = _a % 3
            bx = _b % 3
            ay = int(_a / 3)
            by = int(_b / 3)

            return abs(ax - bx) + abs(ay - by)

        acc = 0
        for x in range(1, 9):
            acc += get_distance_of_two_tiles(self.values.index(x), finalState.values.index(x))

        return acc
    
    # counts how many files have to be moved
    def _distance_difference(self, finalState):
        acc = 0
        for x in range(0, 9):
            acc += 0 if self.values[x] == finalState.values[x] else 1

        return acc

    def equals(self, other):
        return isinstance(other, State) and self.values == other.values

class StateTree:
    class StateTreeNode:
        def __init__(self, state: State):
            self.state = state
            self.parent = None
            self.children = []
        
        def add_child(self, state: State):
            node = StateTree.StateTreeNode(state)
            node.parent = self
            self.children.append(node)
        
        def equals(self, other):
            return isinstance(other, StateTree.StateTreeNode) and self.state.equals(other.state)            

    def __init__(self, initialState: State, finalState: State):
        self.root = StateTree.StateTreeNode(initialState)
        self.currentNode = self.root

        self.finalState = finalState
        self._visitedStates = []
    
    def generate_children_states(self):
        self._visitedStates.append(self.currentNode.state.values)

        sum_tuples = lambda a,b: (a[0]+b[0], a[1]+b[1])

        cn = self.currentNode
        values = cn.state.values
        gap = cn.state.values.index(0)
        gap_pos = ( gap % 3, int(gap / 3) )

        moves = []
        if gap_pos[0] > 0:
            moves.append( (-1, 0) )
        if gap_pos[0] < 2:
            moves.append( ( 1, 0) )
        if gap_pos[1] > 0:
            moves.append( ( 0,-1) )
        if gap_pos[1] < 2:
            moves.append( ( 0, 1) )
        
        gap_dest = []  #where I want to move the gap
        for m in moves:
            target_gap_pos = sum_tuples(gap_pos, m)
            gap_dest.append(target_gap_pos[0] + target_gap_pos[1] * 3)
        
        for s in gap_dest:
            new_list = list( values )
            new_list[gap] = new_list[s]
            new_list[s] = 0

            if new_list not in self._visitedStates:
                cn.add_child(State(new_list))
    
    def get_best_child(self):
        import random

        best = None
        best_score = 999

        for c in self.currentNode.children:
            score = c.state.evaluation_function(self.finalState)
            if score < best_score or (score == best_score and random.randint(1, 100) < 50):
                best_score = score
                best = c

        return best

    def do_interation(self):
        self.generate_children_states()
        self.currentNode = self.get_best_child()

        if self.currentNode == None:
            print('Nothing more to do')
            return False

        myscore = self.currentNode.state.evaluation_function(self.finalState)
        if myscore == 0:
            print('Found solution')
            while self.currentNode.parent != None:
                print(self.currentNode.state.values)
                self.currentNode = self.currentNode.parent

            return False

        #childScore = self.currentNode.state.evaluation_function(self.finalState)
        #if myscore < childScore:
        #    print('Reached local optimal solution')
        #    return False
        
        return True

if __name__ == '__main__':
    initialState = State([0,2,1,6,7,4,3,8,5])
    finalState = State([1,2,3,8,0,4,7,6,5])
    checkedStates = 0

    tree = StateTree(initialState, finalState)
    while tree.do_interation():
        #print('Checking state with score ' + str(tree.currentNode.state.evaluation_function(finalState)))
        #for i in range(0,3):
        #    printline(tree.currentNode.state.values, i*3)
        #print()
        checkedStates += 1

    print(checkedStates)