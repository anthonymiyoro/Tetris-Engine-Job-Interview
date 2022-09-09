import sys, getopt
from multiprocessing import dummy
import numpy as np
from random import choice

import cv2

""" 
This module is a tetris game engine in which a .txt file with the sequence and position of 
tetris shapes is accepted as input and a .txt file with the number of lines remaining at the 
end of the game is produced as output.

Shapes start from the left-most part of the games' grid.
    
Expected Input:
    $ python3 tetris_engine.py <input.txt> output.txt

Returns:
    .txt: Each line containing the number of remaining lines for each line of the input file.
"""

class TetrisEngine:

    # Initialize some variables
    def __init__(self, height, width):
        self.board = np.uint8(np.zeros([height, width, 3]))
        self.place = False
        self.height = height
        self.width = width
        self.drop = True
        self.quit = False
        self.SPEED = 1
        self.flag = 0
        self.held_piece = ""
        

    # All the tetris pieces
    next_piece = choice(["Q", "I", "S", "Z", "L", "J", "T"]) 

    def get_info(self, piece):
        if piece == "I":
            coords = np.array([[0, 0], [0, 1], [0, 2], [0, 3]])
            color = [255, 155, 15]
        elif piece == "T":
            coords = np.array([[0, 0], [0, 1], [0, 2], [1, 1]])
            color = [138, 41, 175]
        elif piece == "L":
            coords = np.array([[0, 0], [1, 0], [2, 0], [2, 1]])
            color = [2, 91, 227]
        elif piece == "J":
            coords = np.array([[0, 1], [1, 1], [2, 1], [2, 0]])
            color = [198, 65, 33]
        elif piece == "Z":
            coords = np.array([[0, 0], [0, 1], [1, 1], [1, 2]])
            color = [55, 15, 215]
        elif piece == "S":
            coords = np.array([[1, 0], [1, 1], [0, 1], [0, 2]])
            color = [1, 177, 89]
        else:
            coords = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
            color = [2, 159, 227]
        return (coords, color)

    def display(self, board, coords, colour, next_info, held_info, SPEED):
        
        # Draw the board
        border = np.uint8(127 - np.zeros([101, 1, 3])) # drawn height? 
        border_ = np.uint8(127 - np.zeros([1, 34, 3])) # drawn width?
        
        dummy = board.copy()
        dummy[coords[:,0], coords[:,1]] = colour
        
        right = np.uint8(np.zeros([101, 10, 3])) # Right border 
        right[next_info[0][:,0] + 2, next_info[0][:,1]] = next_info[1]
        left = np.uint8(np.zeros([101, 10, 3])) # Left border 
        left[held_info[0][:,0] + 2, held_info[0][:,1]] = held_info[1]
        
        dummy = np.concatenate((border, left, border, dummy, border, right, border), 1)
        dummy = np.concatenate((border_, dummy, border_), 0)
        
        dummy = dummy.repeat(101, 0).repeat(101, 1) 
        key = cv2.waitKey(int(1000/SPEED))
        
        return (key)

# Main Loop
if __name__ == "__main__":

    # main
    input_file= sys.argv[1] 
    output_file= sys.argv[2]
    
    game = TetrisEngine(101, 10)
    
    
    # Read input file, loop through each line of input extracting each shapes position
    file1 = open(input_file, 'r')
    input_list = file1.readlines()

    for idx, item in enumerate(input_list): 
        if '\n' in item:
            item = (item.strip())
            input_list[idx] = item

    
    for input_string in input_list:
        input_string_list = input_string.split(",")

        while input_string_list:     
            # Loop through each shape and collect both shape and position
            shape_string = input_string_list[0][0]
            shape_position = input_string_list[0][1]
            next_piece = shape_string
            current_piece = next_piece
            removed_element = input_string_list.pop(0)
            drop = True

            if game.flag > 0:
                game.flag -= 1
            # Determines the color and position of the current, next, and held pieces
            if game.held_piece == "":
                game.held_info = np.array([[0, 0]]), [0, 0, 0]
            else:
                game.held_info = game.get_info(game.held_piece)
            next_info = game.get_info(next_piece)
            coords, color = game.get_info(current_piece)
            coords[:, 1] += int(shape_position) 
            if current_piece == "I":
                top_left = [-2, 3]            
            if not np.all(game.board[coords[:,0], coords[:,1]] == 0):
                break
            while True:
                key = game.display(game.board, coords, color, next_info, game.held_info, game.SPEED)
                dummy = coords.copy() 
                # Checks if the piece is overlapping with other pieces or if it's outside the board, and if so, changes the position to the position before anything happened
                
                if np.max(coords[:,0]) < 101 and np.min(coords[:,0]) >= 0:
                    if not (current_piece == "I" and (np.max(coords[:,1]) >= 10 or np.min(coords[:,1]) < 0)):
                        if not np.all(game.board[coords[:,0], coords[:,1]] == 0):
                            coords = dummy.copy()
                    else:
                        coords = dummy.copy()
                else:
                    coords = dummy.copy()
                    
                if drop:
                    # Finally, we code the “hard drop.” We use a while loop to check if the piece can move one step down, and stop moving down if it collides with an existing piece or
                    # reaches the bottom of the board. 
                    
                    while not game.place:
                        if np.max(coords[:,0]) != 100: 
                            # Checks if the piece is resting on something
                            for pos in coords:
                                if not np.array_equal(game.board[pos[0] + 1, pos[1]], [0, 0, 0]):
                                    game.place = True
                                    break
                        else:
                            # If the position of the piece is at the ground level, then it places
                            game.place = True
                        
                        if game.place:
                            break
                        
                        # Keeps going down and checking when the piece needs to be placed
                        coords[:,0] += 1
                        if current_piece == "I":
                            top_left[0] += 1
                            
                    drop = False
                    
                else:
                    # If we don’t hard drop, then we just need to check if the piece needs to be placed (i.e. stop moving). A piece is placed when the piece either reaches the bottom of the board or hits another piece.

                    # If none of the above cases apply, we move the piece down by one. 
                    # Checks if the piece needs to be placed
                    if np.max(coords[:,0]) != 100:
                        for pos in coords:
                            if not np.array_equal(game.board[pos[0] + 1, pos[1]], [0, 0, 0]):
                                game.place = True
                                break
                    else:
                        game.place = True
                    
                if game.place:
                    # Places the piece where it is on the board
                    for pos in coords:
                        game.board[tuple(pos)] = color
                        
                    # Resets place to False
                    game.place = False
                    break

                # Moves down by 1
                coords[:,0] += 1
                if current_piece == "I":
                    top_left[0] += 1
                    
            # Finally, for each iteration of the outer while loop, (aka each time a piece is placed,)
            # we check if any lines were scored and we update the points.
            
            # Clears lines and also counts how many lines have been cleared and how many left
            # and updates the score every time a block is placed
            lines = 0
            remaining_lines_with_blocks = 0
                    
            # Clear blocks now that a line is full        
            for line in range(101):       
                if np.all([np.any(pos != 0) for pos in game.board[line]]):
                    lines += 1
                    game.board[1:line+1] = game.board[:line]

        
        for line in range(101):      
            # Count number of remaining lines of blocks
            if np.any([np.any(pos != 0) for pos in game.board[line]]):
                remaining_lines_with_blocks = remaining_lines_with_blocks + 1
                
          
        # Clear the blocks and write output
        for unused_var in range(remaining_lines_with_blocks):
            game.board[1:line+1] = game.board[:line]
            
        with open(output_file, "ab") as a:
            a.write((str(remaining_lines_with_blocks)+ "\n").encode())
              
        remaining_lines_with_blocks = 0

                 
        





                                
