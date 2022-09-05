from multiprocessing import dummy
import cv2
import numpy as np
from random import choice

SPEED = 1


#img = np.zeros([height, width, 3], dtype=np.uint8)
board = np.uint8(np.zeros([100,10,3])) # Define the board

# Initialize some variables

quit = False
place = False
drop = False
switch = False
held_piece = ""
flag = 0
score = 0

# All the tetris pieces
next_piece = choice(["Q", "I", "S", "Z", "L", "J", "T"]) # O is Q

def get_info(piece):
    if piece == "I":
        coords = np.array([[0, 0], [0, 1], [0, 2], [0, 3]])
        color = [255, 155, 15]
    elif piece == "T":
        coords = np.array([[1, 0], [1, 1], [1, 2], [0, 1]])
        color = [138, 41, 175]
    elif piece == "L":
        coords = np.array([[1, 0], [1, 1], [1, 2], [0, 2]])
        color = [2, 91, 227]
    elif piece == "J":
        coords = np.array([[1, 0], [1, 1], [1, 2], [0, 0]])
        color = [198, 65, 33]
    elif piece == "S":
        coords = np.array([[1, 2], [1, 1], [0, 0], [0, 1]])
        color = [55, 15, 215]
    elif piece == "Z":
        coords = np.array([[1, 0], [1, 1], [0, 1], [0, 2]])
        color = [1, 177, 89]
    else:
        coords = np.array([[0, 1], [0, 2], [1, 1], [1, 2]])
        color = [2, 159, 227]
    
    return coords, color

def display(board, coords, colour, next_info, held_info, score, SPEED):
    
    # Draw the display
    border = np.uint8(127 - np.zeros([100, 1, 3])) # drawn height? # Change height here
    border_ = np.uint8(127 - np.zeros([1, 34, 3])) # drawn width?
    
    dummy = board.copy()
    dummy[coords[:,0], coords[:,1]] = colour
    
    right = np.uint8(np.zeros([100, 10, 3])) # Right border # Change height here
    right[next_info[0][:,0] + 2, next_info[0][:,1]] = next_info[1]
    left = np.uint8(np.zeros([100, 10, 3])) # Left border # Change height here
    left[held_info[0][:,0] + 2, held_info[0][:,1]] = held_info[1]
    
    dummy = np.concatenate((border, left, border, dummy, border, right, border), 1)
    dummy = np.concatenate((border_, dummy, border_), 0)
    
    dummy = dummy.repeat(100, 0).repeat(100, 1) # Change height here
    dummy = cv2.putText(dummy, str(score), (520, 200), cv2.FONT_HERSHEY_DUPLEX, 1, [0, 0, 255], 2)
    
    
    # Instructions for the player
    dummy = cv2.putText(dummy, "A - move left", (45, 200), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 255])

    dummy = cv2.putText(dummy, "D - move right", (45, 225), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 255])

    dummy = cv2.putText(dummy, "S - move down", (45, 250), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 255])

    dummy = cv2.putText(dummy, "W - hard drop", (45, 275), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 255])

    dummy = cv2.putText(dummy, "J - rotate left", (45, 300), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 255])

    dummy = cv2.putText(dummy, "L - rotate right", (45, 325), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 255])

    dummy = cv2.putText(dummy, "I - hold", (45, 350), cv2.FONT_HERSHEY_DUPLEX, 0.6, [0, 0, 255])
    
    cv2.imshow("Tetris", dummy)
    key = cv2.waitKey(int(1000/SPEED))
    
    return (key)

# Main Loop
if __name__ == "__main__": 
    
    # print(input_list)
    file1 = open('inputs.txt', 'r')
    input_list = file1.readlines()

    for idx, item in enumerate(input_list): # Remove \n
        if '\n' in item:
            item = (item.strip())
            input_list[idx] = item

    print (input_list)
    
    for input_string in input_list:
        input_string_list = input_string.split(",")
    
    while input_string_list:
        # Check if user wants to swap held and current pieces
        if switch:
            # swap held_piece and current_piece
            held_piece, current_piece = current_piece, held_piece
            switch = False
            
        else:
            # Generates the next piece and updates the current piece
            current_piece = next_piece
            shape_string = input_string_list[0][0]
            shape_position = input_string_list[0][1]
            next_piece = shape_string
            removed_element = input_string_list.pop(0)
            # next_piece = choice(["I", "T", "L", "J", "Z", "S", "Q"])

        if flag > 0:
            flag -= 1
        # Determines the color and position of the current, next, and held pieces
        if held_piece == "":
            held_info = np.array([[0, 0]]), [0, 0, 0]
        else:
           held_info = get_info(held_piece)
        next_info = get_info(next_piece)
        coords, color = get_info(current_piece)
        coords[:, 1] += int(shape_position) #Modify coords start positions
        if current_piece == "I":
            top_left = [-2, 3]            
        if not np.all(board[coords[:,0], coords[:,1]] == 0):
            break
        while True:
            key = display(board, coords, color, next_info, held_info, score, SPEED)
            dummy = coords.copy() 
            if key == ord("a"):
                # Moves the piece left if it isn't against the left wall
                if np.min(coords[:,1]) > 0:
                    coords[:,1] -= 1
                if current_piece == "I":
                    top_left[1] -= 1
            elif key == ord("d"):
                # Moves the piece right if it isn't against the right wall
                if np.max(coords[:,1]) < 9:
                    coords[:,1] += 1
                    if current_piece == "I":
                        top_left[1] += 1
                        
            elif key == ord("j") or key == ord("l"):
                # Rotation mechanism
                # arr is the array of nearby points which get rotated and pov is the indexes of the blocks within arr
                
                if current_piece != "I" and current_piece != "Q":
                    if coords[1,1] > 0 and coords[1,1] < 9:
                        arr = coords[1] - 1 + np.array([[[x, y] for y in range(3)] for x in range(3)])
                        pov = coords - coords[1] + 1
                        
                elif current_piece == "I":
                    # The straight piece has a 4x4 array, so it needs seperate code
                    
                    arr = top_left + np.array([[[x, y] for y in range(4)] for x in range(4)])
                    pov = np.array([np.where(np.logical_and(arr[:,:,0] == pos[0], arr[:,:,1] == pos[1])) for pos in coords])
                    pov = np.array([k[0] for k in np.swapaxes(pov, 1, 2)])
                
                # Rotates the array and repositions the piece to where it is now
                
                if current_piece != "Q":
                    if key == ord("j"):
                        arr = np.rot90(arr, -1)
                    else:
                        arr = np.rot90(arr)
                    coords = arr[pov[:,0], pov[:,1]]
            elif key == ord("w"):
                # Hard drop set to true
                drop = True
            elif key == ord("i"):
                # Goes out of the loop and tells the program to switch held and current pieces
                if flag == 0:
                    if held_piece == "":
                        held_piece = current_piece
                    else:
                        switch = True
                    flag = 2
                    break
            elif key == 8 or key == 27:
                quit = True
                break
            
            # Checks if the piece is overlapping with other pieces or if it's outside the board, and if so, changes the position to the position before anything happened
            # CHANGE HEIGHT HERE !!
            if np.max(coords[:,0]) < 100 and np.min(coords[:,0]) >= 0:
                if not (current_piece == "I" and (np.max(coords[:,1]) >= 10 or np.min(coords[:,1]) < 0)):
                    if not np.all(board[coords[:,0], coords[:,1]] == 0):
                        coords = dummy.copy()
                else:
                    coords = dummy.copy()
            else:
                coords = dummy.copy()
                
            if drop:
                #Finally, we code the “hard drop.” We use a while loop to check if the piece can move one step down, and stop moving down if it collides with an existing piece or reaches the bottom of the board. 
                # Every iteration of the loop moves the piece down by 1 and if the piece is resting on the ground or another piece, then it stops and places it
                
                while not place:
                    if np.max(coords[:,0]) != 99: # Change height here
                        # Checks if the piece is resting on something
                        for pos in coords:
                            if not np.array_equal(board[pos[0] + 1, pos[1]], [0, 0, 0]):
                                place = True
                                break
                    else:
                        # If the position of the piece is at the ground level, then it places
                        place = True
                    
                    if place:
                        break
                    
                    # Keeps going down and checking when the piece needs to be placed
                    coords[:,0] += 1
                    score += 1
                    if current_piece == "I":
                        top_left[0] += 1
                        
                drop = False
                
            else:
                # If we don’t hard drop, then we just need to check if the piece needs to be placed (i.e. stop moving). A piece is placed when the piece either reaches the bottom of the board or hits another piece.

                # If none of the above cases apply, we move the piece down by one. 
                # Checks if the piece needs to be placed
                if np.max(coords[:,0]) != 99: # Change height here
                    for pos in coords:
                        if not np.array_equal(board[pos[0] + 1, pos[1]], [0, 0, 0]):
                            place = True
                            break
                else:
                    place = True
                
            if place:
                # Places the piece where it is on the board
                for pos in coords:
                    board[tuple(pos)] = color
                    
                # Resets place to False
                place = False
                break

            # Moves down by 1
            coords[:,0] += 1
            if key == ord("s"):
                score += 1
            if current_piece == "I":
                top_left[0] += 1
                
        # Finally, for each iteration of the outer while loop, (aka each time a piece is placed,)
        # we check if any lines were scored and we update the points.
        
        # Clears lines and also counts how many lines have been cleared and updates the score
        lines = 0
        remaining_lines_with_blocks = 0
                
        for line in range(100): # Change height here         
            if np.all([np.any(pos != 0) for pos in board[line]]):
                lines += 1
                board[1:line+1] = board[:line]
                
            # Count number of remaining lines of blocks
            if np.any([np.any(pos != 0) for pos in board[line]]):
                remaining_lines_with_blocks = remaining_lines_with_blocks + 1
        
                        
        if lines == 1:
            score += 40
        elif lines == 2:
            score += 100
        elif lines == 3:
            score += 300
        elif lines == 4:
            score += 1200
            
        print ("Remaining Lines with Blocks", remaining_lines_with_blocks)


                            
