#
# searcher.py (Final project)
#
# classes for objects that perform state-space search on Eight Puzzles  
#
# name: Kyle
# email: kyley@bu.edu
#
# If you worked with a partner, put his or her contact info below:
# partner's name:
# partner's email:
#

import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    ### Add your Searcher method definitions here. ###
    def __init__(self, depth_limit):
        """ constructs a new Searcher object by initializing 
            the following attributes: states, num_tested, depth_limit
        """
        self.states = []
        self.num_tested = 0
        self.depth_limit = depth_limit


    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s

    
    def should_add(self, state):
        """ returns True if the called Searcher should add state 
            to its list of untested states, and False otherwise.
        """
        
        # if depth is beyond depth limit and # of moves is greater than depth limit
        if self.depth_limit != -1 and state.num_moves > self.depth_limit:
            return False
        
        # if state creates a cycle
        elif state.creates_cycle() == True:
            return False
        
        else:
            return True


    def add_state(self, new_state):
        """ adds state to the Searcher‘s list of untested states. """
        self.states.append(new_state)


    def add_states(self, new_states):
        """ processes the elements of new_states one at a time
            and adds it to the list of untested states. 
        """
        # loops through list of states and adds them one by one
        for s in new_states:
            if self.should_add(s) == True:
                self.add_state(s)


    def next_state(self):
        """ chooses the next state to be tested from the list of 
            untested states, removing it from the list and returning it
        """
        s = random.choice(self.states)
        self.states.remove(s)
        return s


    def find_solution(self, init_state):
        """ performs a full random state-space search, 
            stopping when the goal state is found or 
            when the Searcher runs out of untested states.
        """
        # add the parameter init_state to list
        self.add_state(init_state)
        
        # while loop to find solution
        while self.states != []:
            self.num_tested += 1   # increment
            
            s = self.next_state()
            if s.is_goal():
                return s
            else:
                self.add_states(s.generate_successors())
        return None   # failure



    ### Add your BFSeacher and DFSearcher class definitions below. ###
class BFSearcher(Searcher):
    """ the BFSearcher class inherits from the Searcher class """
    
    def next_state(self):
        """ follows FIFO ordering, which chooses the state
            that has been in the list the longest and removes
            the chosen state from the list of untested states
        """
        s = self.states[0]
        self.states.remove(s)
        return s
    
    
class DFSearcher(Searcher):
    """ the DFSearcher class inherits from the Searcher class """
    
    def next_state(self):
        """ follows LIFO ordering, which chooses the state
            that that was most recently added to the list and removes
            the chosen state from the list of untested states
        """
        s = self.states[-1]
        self.states.remove(s)
        return s
    
    
    
def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

### Add your other heuristic functions here. ###

def h1(state):
    """ a heuristic function that calculates the number of
        misplaced tiles compared to the target state.
    """
    misplaced = state.board.num_misplaced()
    return misplaced


def h2(state):
    """ a heuristic function that calculates the number tiles away
        the misplaced tiles are compared to the target state.
    """
    board = state.board.digit_string()
    target = '012345678'
    distance = 0
    for i in range(9):
        if board[i] != '0':
            tile = int(board[i])
            target_index = target.index(board[i])
            target_row = target_index // 3
            target_col = target_index % 3
            curr_row = i // 3
            curr_col = i % 3
            distance += abs(target_row - curr_row) + abs(target_col - curr_col)

    return distance


class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle and inherits from the Searcher class.
    """
    ### Add your GreedySearcher method definitions here. ###
    def __init__(self, depth_limit, heuristic):
        """ constructor for a GreedySearcher object
            inputs:
             * depth_limit - the depth limit of the searcher
             * heuristic - a reference to the function that should be used 
             when computing the priority of a state
        """
        # add code that calls the superclass constructor
        super().__init__(depth_limit)
        self.heuristic = heuristic


    def priority(self, state):
        """ computes and returns the priority of that state. """
        priority = -1 * self.heuristic(state)
        return priority


    def add_state(self, state):
        """ add a sublist that is a [priority, state] pair, where 
            priority is the priority of state, as determined by 
            calling the priority method.
        """
        priority = self.priority(state)
        sublist = [[priority] + [state]]
        self.states += sublist


    def next_state(self):
        """ chooses one of the states with the highest priority. """
        s = max(self.states)
        self.states.remove(s)
        return s[1]



    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s


### Add your AStarSeacher class definition below. ###

class AStarSearcher(GreedySearcher):
    """ A class for objects that perform an informed A* search on 
        n Eight Puzzle and inherits from the Searcher class.
    """
    def __init__(self, depth_limit, heuristic):
        """ constructor for a AStarSearcher object
            inputs:
             * depth_limit - the depth limit of the searcher
             * heuristic - a reference to the function that should be used 
             when computing the priority of a state
        """
        super().__init__(depth_limit, heuristic)


    def priority(self, state):
        """ computes and returns the priority of that state. """
        heuristic = self.heuristic(state)
        priority = -1 * (heuristic + state.num_moves)
        return priority

    