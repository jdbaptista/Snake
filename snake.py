import tkinter as tk
from random import randint

class Screen:

    def __init__(self, canvas):
        canvas = canvas
        self.menu_screen()
    
    def menu_screen(self):
        canvas.delete("all")
        canvas.create_image(240, 70, image=title)
        canvas.create_image(240, 170, image=play)
        root.bind("<Key>", menu_keys)

    def game_screen(self):
        canvas.delete("all")
        root.bind("<Key>", game_keys)
        direction = "up"
        player = Snake()
        food1 = Food("food1", player)
        food2 = Food("food2", player)
        food3 = Food("food3", player)
        food4 = Food("food4", player)
        food5 = Food("food5", player)
        game_loop(player, food1, food2, food3, food4, food5)

    def end_screen(self, score):
        root.bind("<Key>", end_keys)
        canvas.delete("all")
        canvas.create_image(240, 170, image=play)
        canvas.create_text(240, 240, fill="green", font="Times 20 bold", text="Score: " + str(score))

class Snake:
    
    def __init__(self):
        """Initiates the snake, initial coords at the middle of the canvas and direction of up"""
        self.x = [240]
        self.y = [240]
        self.adding_length = False
        self.length = 1
        self.direction = "up"

    def draw(self):
        """refresh snake and put any changes to attributes to screen"""
        i = self.length
        canvas.delete("Snake")
        while i >= 1:
            canvas.create_rectangle(self.x[i - 1], self.y[i - 1], self.x[i - 1] + 21,
                                         self.y[i - 1] + 21, fill="Green", width=0, tags="Snake")
            i -= 1

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

    def check_food(self, food1, food2, food3, food4, food5):
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

    def __init__(self, tag, player):
        """Defines the food, tag is needed for Tkinter to be able to delete off canvas"""
        Food.counter += 1
        self.x = 0
        self.y = 0
        self.tag = tag
        self.player = player
        self.init_coords(self.player)

    def init_coords(self, player):
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
        canvas.create_rectangle(self.x, self.y, self.x + 21, self.y + 21,
                                     fill="blue", width=0, tags=self.tag)

    def is_eaten(self):
        """Reinitializes the food after it is eaten"""
        # The Snake class deals with checking and adding length
        canvas.delete(self.tag)
        Food.counter -= 1
        self.__init__(self.tag, self.player)

def menu_keys(event):
    if event.keycode == 32:
        screen.game_screen()

def game_keys(event):
    global direction
    if event.keycode == 87:  # key pressed is 'W'
        direction = "up"
    elif event.keycode == 65:  # key pressed is 'A'
        direction = "left"
    elif event.keycode == 83:  # key pressed is 'S'
        direction = "down"
    elif event.keycode == 68:  # key pressed is 'D'
        direction = "right"

def end_keys(event):
    if event.keycode == 32:
        screen.menu_screen()

def game_loop(player, food1, food2, food3, food4, food5, command=""):
    global direction

    if command == "end":
        screen.end_screen(player.length - 1)
        del player
        del food1
        del food2
        del food3
        del food4
        del food5

    if direction == "up" and player.direction != "down":
        player.direction = "up"
    elif direction == "left" and player.direction != "right":
        player.direction = "left"
    elif direction == "down" and player.direction != "up":
        player.direction = "down"
    elif direction == "right" and player.direction != "left":
        player.direction = "right"

    if player.direction == "up" and player.y[0] <= 0:
        game_loop(player, food1, food2, food3, food4, food5, "end")
    elif player.direction == "down" and player.y[0] >= 460:
        game_loop(player, food1, food2, food3, food4, food5, "end")
    elif player.direction == "right" and player.x[0] >= 460:
        game_loop(player, food1, food2, food3, food4, food5, "end")
    elif player.direction == "left" and player.x[0] <= 0:
        game_loop(player, food1, food2, food3, food4, food5, "end")
    else:
        player.movement_logic()
        
        # Check to see if the head of the snake is overlapping any of the other parts
        i = 1
        while i < len(player.x):
            if player.x[0] == player.x[i] and player.y[0] == player.y[i]:
                game_loop(player, food1, food2, food3, food4, food5, "end")
            i += 1

        player.draw()
        food1.draw()
        food2.draw()
        food3.draw()
        food4.draw()
        food5.draw()
        player.check_food(food1, food2, food3, food4, food5)
    root.after(100, lambda: game_loop(player, food1, food2, food3, food4, food5))
                           
if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Snake")
    icon = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, icon)

    canvas = tk.Canvas(root, width=480, height=480, bg="black")
    title = tk.PhotoImage(file="title.png")
    play = tk.PhotoImage(file="play.png")
    canvas.pack()

    screen = Screen(canvas)

    direction = "up"

    root.mainloop()