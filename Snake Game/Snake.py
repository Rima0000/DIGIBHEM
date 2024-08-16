import tkinter as tk
import random
import winsound

# Game settings
WIDTH = 600
HEIGHT = 400
SNAKE_SIZE = 20
SNAKE_SPEED = 150
LEVEL_UP_SCORE = 5
POWER_UP_SCORE = 10
BACKGROUND_COLOR = 'black'
SNAKE_COLOR = 'green'
FOOD_COLOR = 'red'
POWER_UP_COLOR = 'blue'
REPLAY_BUTTON_COLOR = 'orange'
SCORE_FONT = ('Arial', 20)
GAME_OVER_FONT = ('Arial', 24)

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Snake Game")

        self.top_frame = tk.Frame(root, bg=BACKGROUND_COLOR, height=50)
        self.top_frame.pack(fill=tk.X)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        self.score_label = tk.Label(self.top_frame, text=f'Score: 0', font=SCORE_FONT, bg=BACKGROUND_COLOR, fg='white')
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.high_score_label = tk.Label(self.top_frame, text=f'High Score: 0', font=SCORE_FONT, bg=BACKGROUND_COLOR, fg='white')
        self.high_score_label.pack(side=tk.LEFT, padx=10)

        self.difficulty_label = tk.Label(self.top_frame, text=f'Difficulty: Easy', font=SCORE_FONT, bg=BACKGROUND_COLOR, fg='white')
        self.difficulty_label.pack(side=tk.LEFT, padx=10)

        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = 'Right'
        self.food = None
        self.power_up = None
        self.score = 0
        self.level = 1
        self.is_game_over = False
        self.is_paused = False
        self.high_score = 0
        self.power_up_count = 0

        self.create_food()
        self.create_power_up()
        self.update_score()
        self.move_snake()
        self.root.bind('<KeyPress>', self.change_direction)
        self.root.bind('<p>', self.toggle_pause)
        self.root.bind('<r>', self.restart_game)

        self.play_background_music()

    def create_food(self):
        x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        self.food = (x, y)
        self.canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=FOOD_COLOR, tags='food')

    def create_power_up(self):
        if random.random() < 0.1:  # 10% chance to spawn power-up
            x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
            y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
            self.power_up = (x, y)
            self.canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=POWER_UP_COLOR, tags='power_up')

    def update_score(self):
        self.score_label.config(text=f'Score: {self.score}')
        self.high_score_label.config(text=f'High Score: {self.high_score}')
        self.difficulty_label.config(text=f'Difficulty: {self.get_difficulty()}')

    def get_difficulty(self):
        if self.level <= 3:
            return 'Easy'
        elif self.level <= 6:
            return 'Medium'
        else:
            return 'Hard'

    def change_direction(self, event):
        if self.is_paused:
            return
        new_direction = event.keysym
        if new_direction in ['Left', 'Right', 'Up', 'Down']:
            if (new_direction == 'Left' and self.direction != 'Right') or \
               (new_direction == 'Right' and self.direction != 'Left') or \
               (new_direction == 'Up' and self.direction != 'Down') or \
               (new_direction == 'Down' and self.direction != 'Up'):
                self.direction = new_direction

    def move_snake(self):
        if self.is_game_over or self.is_paused:
            return

        head_x, head_y = self.snake[0]
        if self.direction == 'Left':
            head_x -= SNAKE_SIZE
        elif self.direction == 'Right':
            head_x += SNAKE_SIZE
        elif self.direction == 'Up':
            head_y -= SNAKE_SIZE
        elif self.direction == 'Down':
            head_y += SNAKE_SIZE

        new_head = (head_x, head_y)
        if self.check_collision(new_head):
            self.game_over()
            return

        self.snake = [new_head] + self.snake[:-1]
        self.redraw_snake()
        self.check_food()
        self.check_power_up()

        speed = SNAKE_SPEED - (self.level - 1) * 20
        self.root.after(max(speed, 50), self.move_snake)

    def check_collision(self, head):
        x, y = head
        return (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or
                head in self.snake)

    def redraw_snake(self):
        self.canvas.delete('snake')
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=SNAKE_COLOR, tags='snake')

    def check_food(self):
        head = self.snake[0]
        if head == self.food:
            self.snake.append(self.snake[-1])
            self.canvas.delete('food')
            self.create_food()
            self.score += 1
            if self.score % LEVEL_UP_SCORE == 0:
                self.level += 1
            if self.score > self.high_score:
                self.high_score = self.score
            self.update_score()
            self.play_sound('eat.wav')

    def check_power_up(self):
        head = self.snake[0]
        if head == self.power_up:
            self.snake.append(self.snake[-1])
            self.canvas.delete('power_up')
            self.create_power_up()
            self.score += 5
            self.power_up_count += 1
            if self.score > self.high_score:
                self.high_score = self.score
            self.update_score()
            self.play_sound('powerup.wav')

    def toggle_pause(self, event):
        self.is_paused = not self.is_paused
        if not self.is_paused:
            self.move_snake()

    def restart_game(self):
        self.canvas.delete('all')
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = 'Right'
        self.food = None
        self.power_up = None
        self.score = 0
        self.level = 1
        self.is_game_over = False
        self.is_paused = False
        self.power_up_count = 0
        self.create_food()
        self.create_power_up()
        self.update_score()
        self.move_snake()
        if hasattr(self, 'replay_button'):
            self.replay_button.destroy()  # Remove the button

    def game_over(self):
        self.is_game_over = True
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 30, text='Game Over', fill='white', font=GAME_OVER_FONT)
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 30, text=f'Power-Ups Collected: {self.power_up_count}', fill='white', font=SCORE_FONT)
        self.create_replay_button()
        self.update_score()
        self.play_sound('gameover.wav')

    def create_replay_button(self):
        if hasattr(self, 'replay_button'):
            self.replay_button.destroy()  # Remove the button if it already exists
        self.replay_button = tk.Button(self.root, text='Replay', command=self.restart_game, bg=REPLAY_BUTTON_COLOR, fg='white', font=SCORE_FONT)
        self.replay_button.place(x=WIDTH // 2 - 50, y=HEIGHT // 2 + 80, width=100)

    def play_background_music(self):
        # Implement background music playback
        pass

    def play_sound(self, sound_file):
        try:
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
        except Exception as e:
            print(f"Sound error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
