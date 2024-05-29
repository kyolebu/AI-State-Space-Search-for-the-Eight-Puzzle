#
# board.py (Final project)
#
# A Board class for the Eight Puzzle
#
# name: Kyle Yu
# email: kyley@bu.edu
#
# If you worked with a partner, put his or her contact info below:
# partner's name:
# partner's email:
#

class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[0] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1

        # Put your code for the rest of __init__ below.
        # Do *NOT* remove our code above

        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[0])):
                self.tiles[r][c] = int(digitstr[3*r + c])
                if self.tiles[r][c] == 0:
                    self.blank_r = r
                    self.blank_c = c
             
                    
       ### Add your other method definitions below. ###

    def __repr__(self):
        """ This method returns a string representation for the
            object of type Board that it is called on (named self).
        """
        s = ''         # begin with an empty string

        # add one row of slots at a time
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[0])):
                if self.tiles[r][c] == 0:
                    s += '_ '
                else:
                    s += str(self.tiles[r][c]) + ' '
            s += '\n'  # newline at the end of the row
        return s
    
    
    
    def move_blank(self, direction):
        """ takes as input a string direction that specifies 
            the direction in which the blank should move, and 
            that attempts to modify the contents of the called 
            Board object accordingly.
        """
        if direction not in ['up', 'down', 'left', 'right']:
            print(f"unknown direction: {direction}")
            return False
        
        # coordinate values
        coordinate_r = 0
        coordinate_c = 0
        
        # for loop to find blank and update coordinates 
        # according to the direction given
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[0])): 
                
                if self.tiles[r][c] == 0:
                    
                    if direction == 'up':
                        coordinate_r = r - 1
                        coordinate_c = c
                    
                    elif direction == 'down':
                        coordinate_r = r + 1
                        coordinate_c = c
                    
                    elif direction == 'left':
                        coordinate_r = r
                        coordinate_c = c - 1
                    
                    elif direction == 'right':
                        coordinate_r = r
                        coordinate_c = c + 1
                    
        # check if coordinates are on the board
        if coordinate_r not in range(len(self.tiles)) or coordinate_c not in range(len(self.tiles[0])):
            return False
        
        else:
            
            # switching position of 
            self.tiles[self.blank_r][self.blank_c] = self.tiles[coordinate_r][coordinate_c]
            self.tiles[coordinate_r][coordinate_c] = 0
            
            # updating position of blank
            self.blank_r = coordinate_r
            self.blank_c = coordinate_c
            
            return True
        

    def digit_string(self):
        """ creates and returns a string of digits that 
            corresponds to the current contents of the 
            called Board object’s tiles attribute. 
        """
        s = ''
        
        # loop of the string printed by __repr__
        for x in self.__repr__():
            
            if x == '_':   # blank
                s += '0'
                
            elif x not in ['\n', ' ']:   # all numbers
                s += x
        return s



    def copy(self):
        """ returns a newly-constructed Board object 
            that is a deep copy of the called object
        """
        num = self.digit_string()        
        new_board = Board(num)
        return new_board



    def num_misplaced(self):
        """ counts and returns the number of tiles in the 
            called Board object that are not where they 
            should be in the goal state.
        """
        # goal state
        goal = Board('012345678')
        count = 0
        
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[0])): 
                if self.tiles[r][c] == 0:   # discard the blank cell in the count
                    count += 0
                elif self.tiles[r][c] != goal.tiles[r][c]:   # count number of misplaced tiles
                    count += 1
        return count
                    


    def __eq__(self, other):
        """ that overloads the == operator – creating a version 
            of the operator that works for Board objects. 
        """
        return self.tiles == other.tiles
