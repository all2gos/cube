'''Code that creates an object 'cube', which takes in information about a scramble. 
Using various built-in methods of this object, you can obtain information about the state of the cube after applying the scramble.'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

class Cube:
    def __init__(self):
        #creating solved Rubik's cube object
        self.colors = ['W', 'G', 'R', 'B', 'O', 'Y']  #defining side colors: white, green, red, blue, orange, yellow
        self.cube = self.solved_cube()


    def solved_cube(self):
        #'solved' cube: initialization of the main three-dimensional object
        #each side is a 3x3 grid containing letters: W, G, R, B, O, Y
        colors = ['W', 'G', 'R', 'B', 'O', 'Y']  #the order of sides 
        cube = np.array([np.array([f"{color}{i}" for i in range(1, 10)]).reshape(3, 3) for color in colors])
        return cube
    
    def __str__(self):
        return '\n'.join([f"{self.cube[i]}" for i in range(6)])


    def visualize(self, x, y, layout='classic', save_fig_name=''):
        """
        Visualizes the cube in one of two layouts:
        - 'classic': cube net (top, sides, bottom)
        - 'flat': unfolded 18x3 grid
        """
        #mapping letters to colors 
        color_map = {
            'W': 'white',
            'G': 'green',
            'R': 'red',
            'B': 'blue',
            'O': 'orange',
            'Y': 'yellow'
        }



        if layout == 'classic':

            #classic grid layout 
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.axis('off')
            ax.set_xlim(0, 12)
            ax.set_ylim(0, 9)

            #the order of the arrangement of sides on the grid
            positions = {
                0: (3, 6),  #top (white)
                4: (0, 3),  #left (green)
                1: (3, 3),  #front (red)
                2: (6, 3),  #right (blue)
                3: (9, 3),  #back (orange)
                5: (3, 0)   #bottom (yellow)
            }

            #drawing each side:
            for face_idx, (x_offset, y_offset) in positions.items():
                face = self.cube[face_idx]
                for i in range(3):
                    for j in range(3):
                        #get the color and text from a side:
                        cell_value = face[i, j]
                        color = color_map[cell_value[0]]

                        #drawing each sticker:
                        rect = patches.Rectangle(
                            (x_offset + j, y_offset + 2 - i), 
                            1, 1, 
                            facecolor=color,
                            edgecolor='black'
                        )
                        ax.add_patch(rect)

                        #adding text in the center of a sticker:
                        ax.text(
                            x_offset + j + 0.5,         #the center of the sticker on the X-axis
                            y_offset + 2 - i + 0.5,     #the center of the sticker on the Y-axis
                            cell_value,                 #text to display
                            color='black' if color != 'black' else 'white',  #contrasting text color
                            ha='center',                #horizontal alignment
                            va='center',                #vertical alignment
                            fontsize=10                 #font size 
                        )


        elif layout == 'flat':
            #flat 18x3 grid for CNN purposes
            fig, ax = plt.subplots(figsize=(x, y), dpi=100)             
            ax.set_xlim(0, 18)
            ax.set_ylim(0, 3)
            ax.axis('off')

            order_dict = {
                'W': 0,
                'G': 1,
                'R': 2,
                'B': 3,
                'O': 4,
                'Y': 5
            }
            
            flat_list = [
                ['W', 'G', 'R', 'B', 'O', 'Y'],
                ['W', 'O', 'G', 'R', 'B', 'Y'],
                ['W', 'B', 'O', 'G', 'R', 'Y'],
                ['W', 'R', 'B', 'O', 'G', 'Y'], 
                ['G', 'Y', 'R', 'W', 'O', 'B'],
                ['G', 'O', 'Y', 'R', 'W', 'B'],
                ['G', 'W', 'O', 'Y', 'R', 'B'],
                ['G', 'R', 'W', 'O', 'Y', 'B'],
                ['Y', 'B', 'R', 'G', 'O', 'W'],
                ['Y', 'O', 'B', 'R', 'G', 'W'],
                ['Y', 'G', 'O', 'B', 'R', 'W'],
                ['Y', 'R', 'G', 'O', 'B', 'W'],
                ['B', 'W', 'R', 'Y', 'O', 'G'],
                ['B', 'O', 'W', 'R', 'Y', 'G'],
                ['B', 'Y', 'O', 'W', 'R', 'G'],
                ['B', 'R', 'Y', 'O', 'W', 'G'],
                ['R', 'G', 'Y', 'B', 'W', 'O'],
                ['R', 'W', 'G', 'Y', 'B', 'O'],
                ['R', 'B', 'W', 'G', 'Y', 'O'],
                ['R', 'Y', 'B', 'W', 'G', 'O'],
                ['O', 'G', 'W', 'B', 'Y', 'R'],
                ['O', 'Y', 'G', 'W', 'B', 'R'],
                ['O', 'B', 'Y', 'G', 'W', 'R'],
                ['O', 'W', 'B', 'Y', 'G', 'R'],
                ]
            
            random_orientation = random.choice(flat_list)
            x_offset = 0
            
            for face_color in random_orientation:
                face_idx = order_dict[face_color]  #find the index of the side by color
                face = self.cube[face_idx]  #get info about the side
                for i in range(3):
                    for j in range(3):
                        color = color_map[face[i, j][0]]  #find color of the sticker 
                        rect = patches.Rectangle(
                            (x_offset + j, 2 - i), 
                            1, 1, 
                            facecolor=color,
                            edgecolor='black'
                        )
                        ax.add_patch(rect)
                x_offset += 3  #moving to the next section

        if save_fig_name:
            plt.savefig(f'{save_fig_name}.png', bbox_inches='tight', pad_inches=0)


    def rotate(self, front_site):
        #rotate the cube so that the given side is at the front
        #we've found out that two types of rotations and one type of movement are enough to define all the moves on the cube
        temp = self.cube.copy()
        if front_site == 'W':
            self.cube[0] = np.rot90(temp[3],2)
            self.cube[1] = temp[0]
            self.cube[2] = np.rot90(temp[2],1)
            self.cube[3] = np.rot90(temp[5],2 )
            self.cube[4] = np.rot90(temp[4],-1)
            self.cube[5] = temp[1]
        
        elif front_site =='R':
            self.cube[0] = np.rot90(temp[0],-1)
            self.cube[1] = temp[2]
            self.cube[2] = temp[3]
            self.cube[3] = temp[4]
            self.cube[4] = temp[1]
            self.cube[5] = np.rot90(temp[5],1)

    def process_sequence(self, seq):
        seq = seq.split()  # split the sequence of moves into list of separate moves
        s = ""

        for m in seq:
            if len(m) == 2 and m[1] == '2':  #checks if the move is, for example, "L2"
                s += m[0] * 2  #adds the letter twice
            elif len(m) == 2 and m[1] == "'":  #checks if the move is, for example, "F'"
                s += m[0] * 3  #adds the letter three times 
            else:  #single move, for example, "L"
                s += m

        return s
    
    def do(self, seq):
        #the program performs the given sequence on the cube, but it first needs to process it

        for m in seq:
            self.move(m)

    def get_oriented_edges(self):
        '''This function returns a list containing information about oriented edges in the following order:
        -the sum of all oriented edges for the orientation: white bottom, yellow top, green front
        -the number of oriented edges with a white sticker for the orientation: white bottom, yellow top, green front
        -the sum of all oriented edges for the orientation: white bottom, yellow top, red front
        -the number of oriented edges with a white sticker for the orientation: white bottom, yellow top, red front
        ''' 

        oriented_edges_list = []

        if self.cube[0][1, 1] == 'W5' and self.cube[1][1, 1] == 'G5': #check whether the top center sticker is white and the front center sticker is green 
            #get to the orientation: white bottom, yellow top, green front
            self.rotate('R') 
            self.rotate('R')
            self.rotate('W')
            self.rotate('W')
            ''' at this point:
            top center color: Y5
            bottom center color: W5
            front center color: G5
            back center color: B5
            '''

            edge_top_layer_1 = (self.cube[0, 0, 1], self.cube[3, 0, 1]) #for not scrambled cube: yellow/blue
            edge_top_layer_2 = (self.cube[0, 1, 0], self.cube[4, 0, 1]) #yellow/red
            edge_top_layer_3 = (self.cube[0, 2, 1], self.cube[1, 0, 1]) #yellow/green
            edge_top_layer_4 = (self.cube[0, 1, 2], self.cube[2, 0, 1]) #yellow/orange

            edge_middle_layer_1 = (self.cube[3, 1, 2], self.cube[4, 1, 0]) #blue/red
            edge_middle_layer_2 = (self.cube[3, 1, 0], self.cube[2, 1, 2]) #blue/orange
            edge_middle_layer_3 = (self.cube[1, 1, 0], self.cube[4, 1, 2]) #green/red
            edge_middle_layer_4 = (self.cube[1, 1, 2], self.cube[2, 1, 0]) #green/orange

            edge_bottom_layer_1 = (self.cube[5, 2, 1], self.cube[3, 2, 1]) #white/blue
            edge_bottom_layer_2 = (self.cube[5, 1, 0], self.cube[4, 2, 1]) #white/red
            edge_bottom_layer_3 = (self.cube[5, 0, 1], self.cube[1, 2, 1]) #white/green
            edge_bottom_layer_4 = (self.cube[5, 1, 2], self.cube[2, 2, 1]) #white/orange

            edges_top_bottom = [edge_top_layer_1, edge_top_layer_2, edge_top_layer_3, edge_top_layer_4, edge_bottom_layer_1, edge_bottom_layer_2, edge_bottom_layer_3, edge_bottom_layer_4]
            edges_middle = [edge_middle_layer_1, edge_middle_layer_2, edge_middle_layer_3, edge_middle_layer_4]

            oe_top_bottom_green_front = 0
            for edge in edges_top_bottom:
                if any('Y' in element or 'W' in element for element in edge):
                    if 'Y' in edge[0] or 'W' in edge[0]:
                    oe_top_bottom_green_front += 1
                elif any('G' in element or 'B' in element for element in edge):
                    if 'G' in edge[0] or 'B' in edge[0]:
                    oe_top_bottom_green_front += 1

            oe_middle_green_front = 0
            for edge in edges_middle:
                if any('Y' in element or 'W' in element for element in edge):
                    if 'Y' in edge[0] or 'W' in edge[0]:
                        oe_middle_green_front += 1
                elif any('G' in element or 'B' in element for element in edge):
                    if 'G' in edge[0] or 'B' in edge[0]:
                    oe_middle_green_front += 1

            sum_oe_green_front = oe_top_bottom_green_front + oe_middle_green_front
            oriented_edges_list.append(sum_oe_green_front)

            oe_white_sticker_green_front = 0
            for edge in edges_top_bottom:
                if any('W' in element for element in edge):
                    if 'W' in edge[0]:
                        oe_white_sticker_green_front += 1
            for edge in edges_middle:
                if any('W' in element for element in edge):
                    if 'W' in edge[0]:
                        oe_white_sticker_green_front += 1

            oriented_edges_list.append(oe_white_sticker_green_front)

            #get to the orientation: white bottom, yellow top, red front
            self.rotate('R') 
            self.rotate('R')
            self.rotate('R')
            ''' at this point:
            top center color: Y5
            bottom center color: W5
            front center color: R5
            back center color: O5
            '''

            oe_top_bottom_red_front = 0
            for edge in edges_top_bottom:
                if any('Y' in element or 'W' in element for element in edge):
                    if 'Y' in edge[0] or 'W' in edge[0]:
                    oe_top_bottom_red_front += 1
                elif any('R' in element or 'O' in element for element in edge):
                    if 'R' in edge[0] or 'O' in edge[0]:
                    oe_top_bottom_red_front += 1

            oe_middle_red_front = 0
            for edge in edges_middle:
                if any('Y' in element or 'W' in element for element in edge):
                    if 'Y' in edge[0] or 'W' in edge[0]:
                        oe_middle_red_front += 1
                elif any('R' in element or 'O' in element for element in edge):
                    if 'R' in edge[0] or 'O' in edge[0]:
                    oe_middle_red_front += 1

            sum_oe_red_front = oe_top_bottom_red_front + oe_middle_red_front
            oriented_edges_list.append(sum_oe_red_front)

            oe_white_sticker_red_front = 0
            for edge in edges_top_bottom:
                if any('W' in element for element in edge):
                    if 'W' in edge[0]:
                        oe_white_sticker_red_front += 1
            for edge in edges_middle:
                if any('W' in element for element in edge):
                    if 'W' in edge[0]:
                        oe_white_sticker_red_front += 1

            oriented_edges_list.append(oe_white_sticker_red_front)
            
        else:
            print("Wrong orientation, ensure white center is on bottom and green center is on the front.")

        return oriented_edges_list

    def front_move(self):
        #move the front side clockwise
        temp = self.cube.copy()  
        #cube[side, row, column]
        self.cube[0][2, :] = temp[4][:, 2][::-1]  
        self.cube[1] = np.rot90(temp[1],-1)  
        self.cube[2][:, 0] = temp[0,2,0], temp[0,2,1],temp[0,2,2]
        self.cube[4][:, 2] = temp[5][0, :]  
        self.cube[5][0, :] = temp[2,2,0],temp[2,1,0],temp[2,0,0]  

    def move(self, move_type):
        #defining the procedure for executing each move

        if move_type == 'R':
            self.rotate('R') #rotating the cube so that the red side is at the front
            self.front_move() #performing the move
            self.rotate('R') #rotating the cube back
            self.rotate('R') #rotating the cube back
            self.rotate('R') #rotating the cube back
    
        elif move_type == 'B':
            self.rotate('R')
            self.rotate('R')
            self.front_move() #executing the move
            self.rotate('R')
            self.rotate('R')

        elif move_type =='L':
            self.rotate('R')
            self.rotate('R')
            self.rotate('R')
            self.front_move() #executing the move
            self.rotate('R')

        elif move_type == 'F':
            #basic move
            #based on rotation and this move, you can define any other move
            self.front_move() #executing the move

        elif move_type == 'U':
            self.rotate('W') #rotating the cube so that the white side is at the front
            self.front_move() #executing the move
            self.rotate('W') #rotating the cube back
            self.rotate('W') #rotating the cube back
            self.rotate('W') #rotating the cube back


        elif move_type == 'D':
            self.rotate('W') #rotating the cube so that the white side is at the front
            self.rotate('W') #rotating the cube back
            self.rotate('W') #rotating the cube back
            self.front_move() #executing the move
            self.rotate('W') #rotating the cube back



if __name__ == '__main__': #checks if the script is executed as the main program
    cube = Cube() #creates an instance of the Cube class

    #perm U
    #cube.do('RFFFRFRFRFFFRRRFFFRR')
    #cube.do('RUUURURURUUURRRUUURR')
    #cube.do('LBBBLBLBLBBBLLLBBBLL')

    #perm T
    #cube.do(cube.process_sequence("U' B' U2 B2 R2 F2 R U2 R F2 L' F2 L2 U2 B D' F2 L2 F L' U"))
    #cube.process_sequence("RURRRUUURRRFRRUUURRRUUURURRRFFF")
    #cube.do('UU')
    #cube.visualize(layout='flat')
    cube.get_oriented_edges()
    #cube.visualize()
