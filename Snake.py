import tkinter
import random

# ===================== CONSTANTE =====================
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

# ===================== CLASA TILE =====================
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ===================== FEREASTRA JOCULUI =====================
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", height=WINDOW_HEIGHT, width=WINDOW_WIDTH, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# ===================== CENTRAREA ECRANULUI =====================
SCREEN_WIDTH = window.winfo_screenwidth()
SCREEN_HEIGHT = window.winfo_screenheight()

window_x = int((SCREEN_WIDTH / 2) - (WINDOW_WIDTH / 2))
window_y = int((SCREEN_HEIGHT / 2) - (WINDOW_HEIGHT / 2))
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}")

# ===================== VARIABILE GLOBALE =====================
snake = None
food = None
snake_body = []
velocity_x = 0
velocity_y = 0
score = 0
game_over = False

# ===================== SCHIMBAREA DIRECȚIEI =====================
def change_direction(e):  
    global velocity_x, velocity_y

    if e.keysym == "Up" and velocity_y == 0:
        velocity_x = 0
        velocity_y = -1
    elif e.keysym == "Down" and velocity_y == 0:
        velocity_x = 0
        velocity_y = 1
    elif e.keysym == "Right" and velocity_x == 0:
        velocity_x = 1
        velocity_y = 0
    elif e.keysym == "Left" and velocity_x == 0:
        velocity_x = -1
        velocity_y = 0
    elif e.keysym == "space" and game_over:  
        reset_game()  # Restart joc dacă apăsăm Space

# ===================== LOGICA MIȘCĂRII =====================
def move():
    global snake, food, snake_body, score, game_over

    if game_over:
        return

    # Verificare coliziune cu marginile
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return

    # Verificare coliziune cu propriul corp
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # Coliziune cu mâncarea
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    # Actualizare corp șarpe
    if len(snake_body) > 0:
        for i in range(len(snake_body) - 1, 0, -1):
            snake_body[i].x = snake_body[i - 1].x
            snake_body[i].y = snake_body[i - 1].y
        snake_body[0].x = snake.x
        snake_body[0].y = snake.y

    # Mutare cap șarpe
    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE

# ===================== DESENAREA JOCULUI =====================
def draw():
    global game_over

    canvas.delete("all")  # Curățăm ecranul

    if game_over:
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="GAME OVER", fill="red", font=("Arial", 24, "bold"))
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30, text=f"Final Score: {score}", fill="white", font=("Arial", 18, "bold"))
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60, text="Press SPACE to restart", fill="yellow", font=("Arial", 14, "bold"))
        return  

    move()  # Actualizăm pozițiile

    # Desenăm șarpele
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")

    # Desenăm corpul șarpelui
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")

    # Desenăm mâncarea
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")

    # Afișăm scorul
    canvas.create_text(50, 10, text=f"Score: {score}", fill="white", font=("Arial", 14, "bold"))

    window.after(100, draw)  # Reapelăm funcția după 100ms

# ===================== RESTART JOC =====================
def reset_game():
    global snake, food, snake_body, velocity_x, velocity_y, score, game_over

    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)  # Reset capul șarpelui
    food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)  # Reset mâncarea
    snake_body = []
    velocity_x = 0
    velocity_y = 0
    score = 0
    game_over = False

    draw()  # Repornim jocul

# ===================== START JOC =====================
reset_game()  # Inițializare joc
window.bind("<KeyRelease>", change_direction)
window.mainloop()
