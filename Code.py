import pygame
pygame.init()

def algorithm_final(): # Initialising all variables for the initial visualisation
    screen = pygame.display.set_mode((380, 500))
    pygame.display.update()
    pygame.display.set_caption("A* Algorithm Coordinate Picker")
    COLOR_INACTIVE = (100, 100, 100)
    COLOR_ACTIVE = (200, 250, 200)
    GREEN = (196, 162, 220)
    RED = (216, 100, 104)
    BLACK = (0, 0, 0)
    FONT = pygame.font.Font(None, 32)
    start_node_X = pygame.image.load('/Users/brettmcdowell/Downloads/startnodex.png')
    start_node_Y = pygame.image.load('/Users/brettmcdowell/Downloads/startnodey.png')
    end_node_X = pygame.image.load('/Users/brettmcdowell/Downloads/endnodex.png')
    end_node_Y = pygame.image.load('/Users/brettmcdowell/Downloads/endnodey.png')

    def visualisation_final():
        # Initialising variables for Grid and Screen
        Visualisation_Grid = []
        Adjacent_Nodes_Unexplored = []
        Adjacent_Nodes_Explored = []
        A_Star_Path = []
        size_file = open('size.txt', 'r')  # Opening the file containing the size and reading it for the screen size
        file_contents = size_file.readlines()
        size_screen = str(file_contents[0])
        final_size = (size_screen.split('x'))
        final_size = final_size[0]
        Screen_width = int(final_size)
        Screen_height = int(final_size)
        Screen_size = (Screen_width, Screen_height)  # Screen size determined by user
        Visualisation_screen = pygame.display.set_mode(Screen_size)  # Initialising screen to be Screen_size
        pygame.display.set_caption("A* Algorithm Visualisation")  # Caption at top of Screen
        Grid_Horizontal = 50  # Number of rows
        Grid_Vertical = 50  # Number of columns
        # Get X Coordinate by dividing the width of the screen by the number of rows
        X_Co_Ordinate = Screen_width // Grid_Horizontal
        # Get Y Coordinate by dividing the height of the screen by the number of columns
        Y_Co_Ordinate = Screen_height // Grid_Vertical

        # Initialising colours to be used
        Obstruction_Colour = (132, 166, 214)
        Grid_Foreground_Colour = (221, 242, 244)
        Shortest_Path_Colour = (0, 207, 92)
        Adjacent_Nodes_Explored_Colour = (67, 135, 187)
        Adjacent_Nodes_Unexplored_Colour = (242, 207, 92)
        End_Node_Colour = (161, 93, 152)
        Start_Node_Colour = (237, 157, 226)
        Grid_Background_Colour = (70, 120, 130)

        # Grid Set up
        class Grid_Nodes:
            def __init__(self, horizontal_position, vertical_position):
                self.Previous_Node = None  # No previous node as algorithm hasn't begun yet
                self.adjacent_nodes = []  # Empty list
                self.x_coord = horizontal_position  # X coord is on the horizontal position of the node
                self.y_coord = vertical_position  # Y coord is on the vertical position of the node
                self.f_score = 0  # This is how close we are from the start point
                self.g_score = 0  # This is how far from the end node we are
                self.h_score = 0  # This is the combination of the f and g score
                self.Obstacle = False  # No obstalces initially on grid

            def adjacent_node_exploration(self, Visualisation_Grid):
                # This algorithm works by searching all adjacent nodes
                # Going down the grid
                # If row algorithm is less than the total amount of rows - 1
                # then we can move down a row, for example, if there are 70 rows and the algorithm tries to go to row 71 it won't be able to and the programme will crash
                # This procedure prevents that from happening and there isn't any obstacles in the position we want to go to
                if self.x_coord < Grid_Vertical - 1:
                    # Use same column but go a row down and append it to the queue to go to next
                    self.adjacent_nodes.append(Visualisation_Grid[self.x_coord + 1][self.y_coord])
                # Going up the grid
                # If algorithm is not at row 0
                if self.x_coord > 0:
                    # Use same column but go a row up and append it to the queue to go to next
                    self.adjacent_nodes.append(Visualisation_Grid[self.x_coord - 1][self.y_coord])
                # Going right through grid
                # If column algorithm is on is less than the total amount of rows - 1 then we can move right, i.e. it's within bounds
                if self.y_coord < Grid_Horizontal - 1:
                    # Use same row but go a column to the right and append it to the queue to go to next
                    self.adjacent_nodes.append(Visualisation_Grid[self.x_coord][self.y_coord + 1])
                # Going left through grid
                # If our column is greater than 0 then we can keep moving left
                if self.y_coord > 0:
                    # We can append the node to the queue and go there next as we can use the same row but go a column to the left
                    self.adjacent_nodes.append(Visualisation_Grid[self.x_coord][self.y_coord - 1])

            def display_grid_nodes(self, Visualisation_screen, grid_lines):
                if self.Obstacle == True:  # If there is any values in the array of Obstacle
                    grid_lines = Obstruction_Colour  # Set values to Obstruction_Colour
                # Draws node to grid using x coord and y coord as well as size of the node
                pygame.draw.rect(Visualisation_screen, grid_lines, (self.x_coord * X_Co_Ordinate, self.y_coord * Y_Co_Ordinate, X_Co_Ordinate - 1, Y_Co_Ordinate - 1))

        # This function looks at every node in the grid and displays it to the grid
        for horizontal_position in range(Grid_Horizontal):  # For every row in the grid
            Queue = []  # Blank queue for every row in the grid
            for vertical_position in range(Grid_Vertical):  # For every column in the grid
                Queue.append(Grid_Nodes(horizontal_position, vertical_position))  # Append every node to Queue
            Visualisation_Grid.append(Queue)  # Append all nodes in the Queue to the Queue

        # This function looks at every node currently being considered by the algorithm and explores its adjacent nodes
        for horizontal_position in range(Grid_Horizontal):
            for vertical_position in range(Grid_Vertical):
                Visualisation_Grid[horizontal_position][vertical_position].adjacent_node_exploration(Visualisation_Grid)

        # Function reads the coordinates file line by line and inserts them to a list
        final_coordinates = [] # Creating a list of the final coordinates
        file = open('coordinates.txt', 'r') # Opening the file containing the coordinates
        read_file = file.readlines()
        count = 0
        for line in read_file:
            count += 1
            count_ultimate = ("{}: {}".format(count, line.strip()))
            final_coordinates.insert(count, count_ultimate)

        # 4 coordinates each assigned a value within the list
        # Looks through input and splits the list depending on the text beforehand thus allowing values assigned
        # to specific coordinates. For example if the text before the value is Start Node X, it will be split on the ':'
        # and the value after the ':' is assigned the value of the text.
        variable_1 = str((final_coordinates[0]))
        variable_2 = str((final_coordinates[1]))
        variable_3 = str((final_coordinates[2]))
        variable_4 = str((final_coordinates[3]))
        variable_1_split = (variable_1.split(':'))
        if variable_1_split[1] == " Start Node X":
            start_xcoord = int((variable_1_split[2]))
        elif variable_1_split[1] == " Start Node Y":
            start_ycoord = int((variable_1_split[2]))
        elif variable_1_split[1] == " End Node X":
            end_xcoord = int((variable_1_split[2]))
        elif variable_1_split[1] == " End Node Y":
            end_ycoord = int((variable_1_split[2]))

        # Repeats the aforementioned process but for second value in list
        variable_2_split = (variable_2.split(':'))
        if variable_2_split[1] == " Start Node X":
            start_xcoord = int((variable_2_split[2]))
        elif variable_2_split[1] == " Start Node Y":
            start_ycoord = int((variable_2_split[2]))
        elif variable_2_split[1] == " End Node X":
            end_xcoord = int((variable_2_split[2]))
        elif variable_2_split[1] == " End Node Y":
            end_ycoord = int((variable_2_split[2]))

        # Repeats the aforementioned process but for third value in list
        variable_3_split = (variable_3.split(':'))
        if variable_3_split[1] == " Start Node X":
            start_xcoord = int((variable_3_split[2]))
        elif variable_3_split[1] == " Start Node Y":
            start_ycoord = int((variable_3_split[2]))
        elif variable_3_split[1] == " End Node X":
            end_xcoord = int((variable_3_split[2]))
        elif variable_3_split[1] == " End Node Y":
            end_ycoord = int((variable_3_split[2]))

        # Repeats the aforementioned process but for fourth value in list
        variable_4_split = (variable_4.split(':'))
        if variable_4_split[1] == " Start Node X":
            start_xcoord = int((variable_4_split[2]))
        elif variable_4_split[1] == " Start Node Y":
            start_ycoord = int((variable_4_split[2]))
        elif variable_4_split[1] == " End Node X":
            end_xcoord = int((variable_4_split[2]))
        elif variable_4_split[1] == " End Node Y":
            end_ycoord = int((variable_4_split[2]))

        # Clear file after it has been read and values have been assigned
        file = open('coordinates.txt', 'r+')
        file.truncate(0)

        # Assigns the values from the above process to variables, that will later be used to display the start and
        # end node on the grid
        start_xcoord_1 = start_xcoord
        start_ycoord_1 = start_ycoord
        end_xcoord_1 = end_xcoord
        end_ycoord_1 = end_ycoord

        # Calculates manhattan distance between two coordinates, used for g score
        def Manhattan_Distance(Position_One, Position_Two):
            return abs(Position_One.x_coord - Position_Two.x_coord) + abs(Position_One.y_coord - Position_Two.y_coord)
            # Returns distance between two coordinates
            # Firstly, calculates distance between two x coordinates
            # Secondly, calculates distance between two y coordinates
            # Returns this value useful for g score

        Start_Node = Visualisation_Grid[start_xcoord_1][start_ycoord_1]  # Position of Start Node on grid
        Adjacent_Nodes_Unexplored.append(Start_Node)  # Making sure algorithm starts at Start Node
        End_Node = Visualisation_Grid[end_xcoord_1][end_ycoord_1]  # Position of End Node on grid

        def User_Obstructions(cursor_position, exploration_status):  # Displaying user's input that creates the obstructions for the path
            # Here we're saying that the cursor position divided by the X co-ordinate is where the obstruction's x coordinate is and the same for the y coordinate
            horizontal_position = cursor_position[0] // X_Co_Ordinate
            vertical_position = cursor_position[1] // Y_Co_Ordinate
            # Here we're saying that the x and y coordinate of the grid become the obstacle and this changes the status of the node
            Visualisation_Grid[horizontal_position][vertical_position].Obstacle = exploration_status

        def Logic_Loop():  # Main logic loop for commencing algorithm
            main_flag = False
            algorithm_flag = False
            while True:  # Will continue to be true allowing program to continue
                Visualisation_screen.fill(Grid_Background_Colour)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # If quit is pressed it will quit
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:  # If a key is pressed
                        if event.key == pygame.K_RETURN:  # If return is pressed
                            algorithm_flag = True  # Algorithm begins
                    if event.type == pygame.MOUSEMOTION:  # If mouse is moving
                        if pygame.mouse.get_pressed()[0]:  # If left button on mouse is clicked
                            if algorithm_flag == False:  # If the algorithm has not begun yet
                                Mouse_Position = pygame.mouse.get_pos()  # Gets the position of the mouse
                                # We will feed Mouse_Position into our obstacle procedure so that whenever the mouse button is pressed
                                # by the user an obstacle will be displayed onto the grid. The validation here is that it can
                                # only happen before the algorithm has begun.
                                # We feed in true to the function so that it's displayed to the grid constantly
                                User_Obstructions(Mouse_Position, True)

                def Display_Nodes():  # Displaying all nodes to the grid
                    for horizontal_position in range(Grid_Horizontal):  # For every horizontal position in the grid
                        for vertical_position in range(Grid_Vertical):  # For every vertical position in the grid
                            Node = Visualisation_Grid[vertical_position][horizontal_position]  # Node is the x and y of the for loops
                            # Displaying all nodes to the screen with the colour of Grid_Foreground_Colour
                            Node.display_grid_nodes(Visualisation_screen, Grid_Foreground_Colour)  # Display all nodes to screen
                            if Node in A_Star_Path:  # If a node is in the shortest path then display it in a specific colour
                                Node.display_grid_nodes(Visualisation_screen, Shortest_Path_Colour)  # Specific colour is green
                            elif Node in Adjacent_Nodes_Explored:  # If a node has been explored set to a specific colour
                                Node.display_grid_nodes(Visualisation_screen,Adjacent_Nodes_Explored_Colour)  # Specific colour is a shade of blue
                            elif Node in Adjacent_Nodes_Unexplored:  # If a node has not been explored it's set to a specific colour
                                Node.display_grid_nodes(Visualisation_screen,Adjacent_Nodes_Unexplored_Colour)  # Specific colour is a shade of yellow
                            try:  # This allows the start node and end node to always be displayed
                                if Node == Start_Node:
                                    Node.display_grid_nodes(Visualisation_screen, Start_Node_Colour)
                                if Node == End_Node:
                                    Node.display_grid_nodes(Visualisation_screen, End_Node_Colour)
                            except Exception:  # This just passes meaning that the start and end node will be displayed with no exception
                                pass

                Display_Nodes()  # Displays nodes to grid

                # Getting into logic of actual algorithm
                if algorithm_flag == True:  # If the algorithm has begun
                    shortest_node = 0  # Shortest Node is not known yet
                    for x in range(len(Adjacent_Nodes_Unexplored)):  # For every node in the unexplored adjacent nodes list
                        # If the f score of the adjacent node is less than the f score of the shortest node then it becomes the shortest node
                        # Essentially, we're comparing to see if the adjacent node is a shorter distance from the start point
                        if Adjacent_Nodes_Unexplored[x].f_score < Adjacent_Nodes_Unexplored[shortest_node].f_score:
                            shortest_node = x
                    # The next node to be explored is the shortest node from the unexplored adjacent nodes, i.e. the result
                    # of the above equation
                    next_node = Adjacent_Nodes_Unexplored[shortest_node]
                    if main_flag == False:  # If the algorithm has not finished yet
                        # Remove the shortest_node from the unexplored list and put it into the explored list
                        # This way the algorithm continues to look at unexplored nodes
                        Adjacent_Nodes_Unexplored.remove(next_node)
                        Adjacent_Nodes_Explored.append(next_node)
                        # Essentially we will then look at the next adjacent node in the list
                        for adjacent_node in next_node.adjacent_nodes:  # For the adjacent node in the adjacent nodes list
                            # If the adjacent node has already been explored or is an obstacle then continue
                            if adjacent_node in Adjacent_Nodes_Explored or adjacent_node.Obstacle:
                                continue
                            Temporary_G_Score = next_node.g_score  # The temporary g score is the next nodes g score
                            Final_Path = False  # The final path has not been discovered yet
                            if adjacent_node in Adjacent_Nodes_Unexplored:
                                if Temporary_G_Score < adjacent_node.g_score:  # If the next node's g score is less than the adjacent node's g score
                                    # I.e. if the next node is closer to the end node than the adjacent node
                                    adjacent_node.g_score = Temporary_G_Score  # Its g node is considered as it's less, i.e. closer
                                    Final_Path = True
                            else:  # If the adjacent node is explored
                                adjacent_node.g_score = Temporary_G_Score  # The adjacent node to the explored node becomes the next node to be considered
                                Final_Path = True
                                Adjacent_Nodes_Unexplored.append(adjacent_node)  # The adjacent node is appended to the unexplored nodes
                                # It will be explored next
                            if Final_Path == True:  # If a final path has been discovered
                                # Calculating manhattan distance between the adjacent node and the end point
                                adjacent_node.Y_Co_Ordinate = Manhattan_Distance(adjacent_node, End_Node)
                                adjacent_node.f_score = adjacent_node.g_score + adjacent_node.Y_Co_Ordinate
                                # The previous node that was put on the final path is the next node to be looked at
                                adjacent_node.Previous_Node = next_node

                    if next_node == End_Node:  # If the next node to be discovered is the end node then the algorithm has been completed
                        Temporary_Node = next_node
                        while Temporary_Node.Previous_Node:  # While the temporary node is the previous node
                            A_Star_Path.append(Temporary_Node.Previous_Node)  # Appending the shortest previous node to the final path
                            Temporary_Node = Temporary_Node.Previous_Node  # Temporary node is the final path node
                        if main_flag == False:  # If the main flag is false, i.e. the program hasn't begun
                            main_flag = True  # Set it true
                        elif main_flag == True:  # If it's true
                            continue  # Continue with the algorithm

                pygame.display.update()  # Update the display

        Logic_Loop()

    # Procedure for displaying buttons to the screen
    # Takes in x and y coordinate, then width and height of button, and then the active colour, i.e. the colour
    # the button will go when the mouse is hovered over it and the inactive colour is the colour of the button when
    # it's not being hovered over
    def button(x, y, w, h, ac, ic):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # If the position of the mouse is within the button's boundaries it will go active
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, ((x, y, w, h)))
            if click[0] == 1: # If a button is clicked then it will proceed
                visualisation_final()
        else: # If the position of the mouse is not within the button's boundaries it will be inactive
            pygame.draw.rect(screen, ic, (x, y, w, h))

    # Procedure that renders the text to the screen
    def text_objects(text, font):
        textSurface = font.render(text, True, BLACK)
        return textSurface, textSurface.get_rect()

    # Procedure that formats the text and the position of the text on the screen
    def displayText(message, x, y, font_size):
        smallText = pygame.font.Font("freesansbold.ttf", font_size)
        textSurf, textRect = text_objects(message, smallText)
        textRect.center = (x, y)
        screen.blit(textSurf, textRect)

    # Class for the input box for coordinates to be entered
    class InputBox:
        # Instances of the input box will use the x and y coordinate and the width and height.
        # The text being blank allows users to input what they want into the text box.
        def __init__(self, x, y, w, h, text=''):
            self.rect = pygame.Rect(x, y, w, h)
            self.color = COLOR_INACTIVE
            self.text = text
            self.txt_surface = FONT.render(text, True, self.color)
            self.active = False

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            if event.type == pygame.KEYDOWN: # If pressed a key
                if self.active: # If the input box is active
                    if event.key == pygame.K_RETURN: # Whatever the user inputs is written to the text file
                        # when the return button is pressed
                        file = open('coordinates.txt', 'a')
                        file.write(str(self.text))
                        file.write('\n')
                        file.close()
                        self.text = ('')
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1] # If the user presses the back button the previous character is removed
                    else:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = FONT.render(self.text, True, self.color)

        # Updates the input box
        def update(self):
            width = max(200, self.txt_surface.get_width() + 10)
            self.rect.w = width

        # Displays the proceed button to the screen
        def draw(self, screen):
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
            pygame.draw.rect(screen, self.color, self.rect, 2)
            screen.blit(start_node_X, (9, 10))
            screen.blit(start_node_Y, (9, 110))
            screen.blit(end_node_X, (9, 210))
            screen.blit(end_node_Y, (9, 310))
            button(30, 415, 320, 50, GREEN, RED)
            displayText("Proceed to visualisation", 190, 440, 24)

    # Displays the input boxes to the screen by displaying them as instances of the class
    def main():
        input_box1 = InputBox(90, 50, 140, 32, 'Start Node X: ')
        input_box2 = InputBox(90, 150, 140, 32, 'Start Node Y: ')
        input_box3 = InputBox(90, 250, 140, 32, 'End Node X: ')
        input_box4 = InputBox(90, 350, 140, 32, 'End Node Y: ')
        input_boxes = [input_box1, input_box2, input_box3, input_box4]
        finished = False

        # If the event in pygame is quit then the coordinates file is written clean
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                    file = open('coordinates.txt', 'r+')
                    file.truncate(0)
                for box in input_boxes: # Handles the input of the input boxes
                    box.handle_event(event)
            # Update input boxes
            for box in input_boxes:
                box.update()
            # Displays input boxes to the screen
            screen.fill((142, 164, 200))
            for box in input_boxes:
                box.draw(screen)
            # Updates screen so input boxes are visible
            pygame.display.update()

    main()

# Screen that allows the user to pick the size of the grid for the visualisation
def visualisation_creator():
    # Initialising variables
    creation = True
    creator_width = 500
    creator_height = 500
    TitleBlue = (19,37,77)
    WHITE = (255,255,255)
    IC_GOLD = (139,125,51)
    AC_GOLD = (203,192,40)
    creator = pygame.display.set_mode((creator_width,creator_height))
    pygame.display.set_caption('Visualisation Screen Creator')
    creator.fill(TitleBlue)
    pygame.draw.rect(creator, IC_GOLD, (5,5,490,30))
    pygame.draw.rect(creator, IC_GOLD, (10,317,475,172))
    pygame.display.update()

    # Procedure for the buttons, if the mouse position is within the boundaries then they are made active
    # if they are active and they are pressed then the text displayed on the button is written to a text file and this
    # is used for the size of the visualisation. If the mouse position is outside the boundaries of the button then
    # it's inactive and it will be displayed the inactive colour
    def button(x,y,w,h,ac,ic,message):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(creator, ac, ((x, y, w, h)))
            if click[0] == 1:
                file = open('size.txt', 'w')
                file.write(str(message))
                file.close()
                algorithm_final()
        else:
            pygame.draw.rect(creator, ic, (x, y, w, h))

    # Procedures for displaying the text to the screen and formatting the text
    def text_objects(text, font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()
    def displayText(message,x,y,font_size):
        smallText = pygame.font.Font("freesansbold.ttf",font_size)
        textSurf, textRect = text_objects(message,smallText)
        textRect.center = (x,y)
        creator.blit(textSurf, textRect)
    # Displaying image to the screen
    displayText("Please select which one of the width and heights you would like for your visualisation",250,20,12)
    logoImg = pygame.image.load('/Users/brettmcdowell/Downloads/Logo.png')
    creator.blit(logoImg,(40,325))

    # While the creation variable is true the buttons and corresponding text will be displayed to the screen
    while creation:
        for event in pygame.event.get():
            button(75,60,100,30,AC_GOLD,IC_GOLD,"300x300")
            button(325,60,100,30,AC_GOLD,IC_GOLD,"400x400")
            button(75,160,100,30,AC_GOLD,IC_GOLD,"500x500")
            button(325,160,100,30,AC_GOLD,IC_GOLD,"600x600")
            button(200,235,100,30,AC_GOLD,IC_GOLD,"700x700")
            displayText("300x300",125,75,22)
            displayText("400x400",375,75,22)
            displayText("500x500",125,175,22)
            displayText("600x600",375,175,22)
            displayText("700x700",250,250,22)
            pygame.display.update()
            if event.type == pygame.QUIT:
                creation = False
                pygame.quit()
                quit()
    pygame.display.update()

# Main program for the intro screen that displays information about the A* algorithm and how it works etc.
def intro_screen():
    # Initialising variables
    intro_screen = True
    Screen_width = 1425
    Screen_height = 700
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    BGREEN = (0,255,0)
    DGREEN = (0,160,0)
    # Loading images to the screen and setting screen size
    algoImg = pygame.image.load('/Users/brettmcdowell/Downloads/algorithm.png')
    lineImg = pygame.image.load('/Users/brettmcdowell/Downloads/Blackline.png')
    lineImg2 = pygame.image.load('/Users/brettmcdowell/Downloads/Blackline.png')
    horizontalLine = pygame.image.load('/Users/brettmcdowell/Downloads/Line2.png')
    MazeImg = pygame.image.load('/Users/brettmcdowell/Downloads/Maze.png')
    NavImg1 = pygame.image.load('/Users/brettmcdowell/Downloads/Nav7.png')
    screen = pygame.display.set_mode((Screen_width, Screen_height))
    pygame.display.set_caption('A* Algorithm Visualisation Introduction')
    screen.fill(WHITE)
    # Displaying images to the screen
    screen.blit(algoImg,(17,50))
    screen.blit(lineImg,(120,0))
    screen.blit(lineImg2,(600,0))
    screen.blit(horizontalLine,(595,0))
    screen.blit(MazeImg,(1150,90))
    screen.blit(NavImg1,(1175,280))
    pygame.display.update()

    # Procedure previously used for the button, if the button is pressed it will move onto the next screen and be displayed
    # as an active colour if not it will be an inactive colour
    def button(x,y,w,h,ac,ic):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, ((x, y, w, h)))
            if click[0] == 1:
                visualisation_creator()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))

    # Procedure for displaying text to screen
    def text_objects(text, font):
        textSurface = font.render(text, True, BLACK)
        return textSurface, textSurface.get_rect()
    # Procedure for formatting the text
    def displayText(message,x,y,font_size):
        smallText = pygame.font.Font("freesansbold.ttf",font_size)
        textSurf, textRect = text_objects(message,smallText)
        textRect.center = (x,y)
        screen.blit(textSurf, textRect)

    # Displaying the text to screen with an x and y coordinate and a font size
    displayText("Welcome to the A* Algorithm Visualisation",280,25,25)
    displayText("The A* algorithm is a graph traversal and path search algorithm which is often",280,450,14)
    displayText("used in many fields of computer science due to its completeness, optimality",280,475,14)
    displayText("and optimal efficiency. However, one disadvantage is its space complexity",280,500,14)
    displayText("as it stores all generated nodes in memory. Thus, in practical navigation",280,525,14)
    displayText("systems, it is generally outperformed by algorithms which can pre-process the",280,550,14)
    displayText("graph to attain better peformance, as well as memory-bounded approaches.",280,575,14)
    displayText("However, the A* pathfinding algorithm is still the best-performing algorithm",280,600,14)
    displayText("in many cases. The algorithm has many real-life practical application",280,625,14)
    displayText("including: navigation systems and in video-games as maze solvers.",280,650,14)
    displayText("My system will visualise the A* algorithm based on user-input.",280,675,14)
    displayText("How the algorithm works",810,20,30)
    displayText("A* is an informed search algorithm/best-first search meaning it is",810,85,13)
    displayText("formulated in terms of weighted graphs: starting from a specific starting",810,105,13)
    displayText("node of a graph, it aims to find a path to the given goal node having",810,125,13)
    displayText("the smallest cost. It does this by maintaining a tree of paths",810,145,13)
    displayText("originating at the start node and extending paths one edge at a time",810,165,13)
    displayText("until its termination criterion is satisfied. At each iteration of its",810,185,13)
    displayText("main loop, A* needs to determine which of its paths to extend. It",810,205,13)
    displayText("does so based on the cost of the path and an estimate of the cost",810,225,13)
    displayText("required to extend the path all the way to the goal. Specifically,",810,245,13)
    displayText("A* selects the path that minimises the time complexity where n is the",810,265,13)
    displayText("next node on the path, g(n) is the cost of the path from the start node",810,285,13)
    displayText("to n and h(n) is a heuristic function that estimates the cost of the",810,305,13)
    displayText("cheapest path from n to the goal. A* terminates when the path it",810,325,13)
    displayText("chooses to extend is the path from start to goal or if there are no",810,345,13)
    displayText("paths to be extended. Typical A* implementations use a priority queue",810,365,13)
    displayText("to perform the repeated selection of minimum cost nodes to expand. At",810,385,13)
    displayText("each step of the algorithm, the node with the lowest f(x) value is",810,405,13)
    displayText("removed from the queue, the f and g values of its neighbours are",810,425,13)
    displayText("updates accordingly, and these neighbours are added to the queue.",810,445,13)
    displayText("The algorithm continues until a removed node is the goal node. ",810,465,13)
    displayText("The f value of that goal is then also the cost of the shortest",810,485,13)
    displayText("path. When researching this project I contacted my intended end",810,505,13)
    displayText("users of AQA A Level Computer Science students and an A* algorithm",810,525,13)
    displayText("industry expert. Both of these groups brought it to my attention",810,545,13)
    displayText("that some reference to time complexity and A* being a modificiation",810,565,13)
    displayText("of Dijkstra's algorithm might be useful as to contextualise the ",810,585,13)
    displayText("A* algorithm with relation to Dijkstra's algorithm. The time complexity",810,605,13)
    displayText("of the A* pathfinding algorithm is hard to calculate but the worst-case",810,625,13)
    displayText("space complexity/performance of O(b^D) is assumed for A*. The A*",810,645,13)
    displayText("algorithm modifies the heuristic of Dijkstra by adding a general direction",810,665,13)
    displayText("of the end node. As such the A* algorithm is a modification of Dijkstra. ",810,685,13)
    displayText("Implementations",1250,15,24)
    displayText("Implementations of the A* algorithm include navigation",1245,40,12)
    displayText("systems and maze-solvers in video games, below are two",1245,60,12)
    displayText("images of such implementations. Maze-Solver in a video game:",1245,80,12)
    displayText("Click the green button to proceed to the A* Visualisation:",1245,620,12)
    displayText("Below are navigation system examples that may use A* algorithm:",1245,270,11)
    displayText("The above navigation system is a good example of the",1245,560,12)
    displayText("usefulness of the A* algorithm, through the user inputting",1245,580,12)
    displayText("two points it will find the shortest path on the roads.",1245,600,12)
    pygame.display.update()

    # While the intro_screen variable is true, i.e. while on the intro screen
    while intro_screen:
        for event in pygame.event.get(): # Displays buttons to screen and text in button
            button(1066.5, 635, 355.5, 55, BGREEN, DGREEN)
            displayText("PROCEED TO VISUALISATION", 1240, 665, 20)
            pygame.display.update()
            # If the quit button is pressed, quit the function
            if event.type == pygame.QUIT:
                intro_screen = False
                pygame.quit()
                quit()
    pygame.display.update()
# Carries out the intro_screen procedure
intro_screen()
