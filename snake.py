import tkinter as tk
from random import randint

class Snake:
    """ The main player """

    def __init__(self):
        """Initiates the snake, initial coords at the middle of the canvas and direction of up"""
        self.x = [240]
        self.y = [240]
        self.adding_length = False
        self.length = 1
        self.direction = "up"

    def update(self):
        """Binds the snake to Refresh()"""
        self.movement_logic()
        self.self_detection()
        self.draw()

    def draw(self):
        """refresh snake and put any changes to attributes to screen"""
        i = self.length
        game_canvas.delete("Snake")
        while i >= 1:
            game_canvas.create_rectangle(self.x[i - 1], self.y[i - 1], self.x[i - 1] + 21,
                                         self.y[i - 1] + 21, fill="Green", width=0, tags="Snake")
            i -= 1

    def self_detection(self):
        """Check to see if the head of the snake is overlapping any of the other parts"""
        i = 1
        while i < len(self.x):
            if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                end()
            i += 1

    def movement_logic(self):
        """Moves each part of the snake, following the head moving in a specified direction"""
        i = self.length
        temp_x_0 = self.x[0]
        temp_y_0 = self.y[0]
        if self.adding_length:
            self.length += 1
            self.adding_length = False
        else:
            self.x.pop(i - 1)
            self.y.pop(i - 1)
        if self.direction == "up":
            self.x.insert(0, temp_x_0)
            self.y.insert(0, temp_y_0 - 20)
        if self.direction == "down":
            self.x.insert(0, temp_x_0)
            self.y.insert(0, temp_y_0 + 20)
        if self.direction == "right":
            self.x.insert(0, temp_x_0 + 20)
            self.y.insert(0, temp_y_0)
        if self.direction == "left":
            self.x.insert(0, temp_x_0 - 20)
            self.y.insert(0, temp_y_0)

    def check_food(self):
        """Checks to see if the snake has eaten any of the 5 foods"""
        if self.x[0] == food1.x and self.y[0] == food1.y:
            food1.is_eaten()
            self.adding_length = True
        if self.x[0] == food2.x and self.y[0] == food2.y:
            food2.is_eaten()
            self.adding_length = True
        if self.x[0] == food3.x and self.y[0] == food3.y:
            food3.is_eaten()
            self.adding_length = True
        if self.x[0] == food4.x and self.y[0] == food4.y:
            food4.is_eaten()
            self.adding_length = True
        if self.x[0] == food5.x and self.y[0] == food5.y:
            food5.is_eaten()
            self.adding_length = True

class Food:
    counter = 0

    def __init__(self, tag):
        """Defines the food, tag is needed for Tkinter to be able to delete off canvas"""
        Food.counter += 1
        self.x = 0
        self.y = 0
        self.tag = tag
        self.init_coords()
        self.draw()

    def init_coords(self):
        """Finds suitable coordinates for the food, if none is found the food is deleted forever"""
        space = 576 - player.length - Food.counter
        if space <= 0:
            del self
        else:
            while True:
                self.x = randint(0, 23) * 20
                self.y = randint(0, 23) * 20
                searching_tally = 0
                i = player.length
                while i >= 1:
                    if not (self.x == player.x[i-1] and self.y == player.y[i-1]):
                        searching_tally += 1
                        i -= 1
                    else:
                        i -= 1
                if searching_tally == player.length:
                    break

    def draw(self):
        game_canvas.create_rectangle(self.x, self.y, self.x + 21, self.y + 21,
                                     fill="blue", width=0, tags=self.tag)

    def is_eaten(self):
        """Reinitializes the food after it is eaten"""
        # The Snake class deals with checking and adding length
        game_canvas.delete(self.tag)
        Food.counter -= 1
        self.__init__(self.tag)

def key(event):
    """Key bindings"""
    global direction
    if event.keycode == 87 and player.direction != "down":  # key pressed is 'W'
        direction = "up"
    elif event.keycode == 65 and player.direction != "right":  # key pressed is 'A'
        direction = "left"
    elif event.keycode == 83 and player.direction != "up":  # key pressed is 'S'
        direction = "down"
    elif event.keycode == 68 and player.direction != "left":  # key pressed is 'D'
        direction = "right"

def Refresher_init():
    global player
    global food1
    global food2
    global food3
    global food4
    global food5
    global direction

    direction = "up"
    # create the player
    player = Snake()

    # create the food
    food1 = Food("food1")
    food2 = Food("food2")
    food3 = Food("food3")
    food4 = Food("food4")
    food5 = Food("food5")

    # establish game loop and key binds
    root.bind("<Key>", key)
    Refresher()

def Refresher():
    global player
    global food1
    global food2
    global food3
    global food4
    global food5
    """The main game loop, refreshing the canvas every 100 milliseconds"""
    # should change this so that the frame rate and player movement speed are separate
    if direction == "up" and player.y[0] <= 0:
        end()
    elif direction == "down" and player.y[0] >= 460:
        end()
    elif direction == "right" and player.x[0] >= 460:
        end()
    elif direction == "left" and player.x[0] <= 0:
        end()
    else:
        player.direction = direction
        player.update()
        player.check_food()
    root.after(100, Refresher)

def menu_keys(event):
    global choice
    if event.keycode == 32:
        choice = "game"


def main_menu():
    if choice == "game":
        game_canvas.delete("all")
        Refresher_init()
    else:
        root.after(100, main_menu)

def end():
    global player
    global food1
    global food2
    global food3
    global food4
    global food5
    global choice
    global title
    global game_canvas
    global w_key
    game_canvas.delete("all")

    title = tk.PhotoImage(file="title.png")
    game_canvas.create_image(240, 70, image=title)

    w_key = tk.PhotoImage(file="play.png")
    game_canvas.create_image(240, 170, image=w_key)

    game_canvas.create_text(240, 240, fill="green", font="Times 20 italic bold", text="Score: " + str(player.length - 1))
    choice = ""

    del player
    del food1
    del food2
    del food3
    del food4
    del food5

    root.bind("<Key>", menu_keys)
    main_menu()
    

if __name__ == "__main__":
    # create the window
    root = tk.Tk()
    root.title("Snake")
    # icon = tk.PhotoImage(file="snake_icon.gif")
    # root.iconphoto(False, icon)
    game_canvas = tk.Canvas(root, width=480, height=480, bg="black")
    game_canvas.pack()

    title = tk.PhotoImage(file="title.png")
    game_canvas.create_image(240, 70, image=title)

    w_key = tk.PhotoImage(file="play.png")
    game_canvas.create_image(240, 170, image=w_key)

    choice = ""
    direction = "up"

    root.bind("<Key>", menu_keys)
    main_menu()

    root.mainloop()
