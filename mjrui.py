from color import Color
from game import Game
import tkinter as tk
from tkinter import ttk
import threading

class SimulationGUI:
    def __init__(self, root):
        self.game = None
        self.root = root
        self.root.title("Game Simulation")
        
        # Progress frame
        progress_frame = ttk.Frame(root, padding="10")
        progress_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.progress_var = tk.DoubleVar()
        self.progress_label = ttk.Label(progress_frame, text="Simulation Progress:")
        self.progress_label.grid(row=0, column=0, sticky=tk.W)
        self.progress_bar = ttk.Progressbar(progress_frame, length=300, mode='determinate', variable=self.progress_var)
        self.progress_bar.grid(row=1, column=0, pady=5)
        
        # Results frame
        self.results_text = tk.Text(root, height=15, width=50)
        self.results_text.grid(row=1, column=0, padx=10, pady=5)

        self.player_1_text = tk.Text(root, height=1, width=50)
        self.player_1_text.grid(row=3, column=0, padx=10, pady=0)
        
        self.player_2_text = tk.Text(root, height=1, width=50)
        self.player_2_text.grid(row=4, column=0, padx=10, pady=0)
        
        self.player_3_text = tk.Text(root, height=1, width=50)
        self.player_3_text.grid(row=5, column=0, padx=10, pady=0)
        
        self.player_4_text = tk.Text(root, height=1, width=50)
        self.player_4_text.grid(row=6, column=0, padx=10, pady=0)
        
        # Create board frame
        board_frame = ttk.Frame(root, padding="10")
        board_frame.grid(row=0, column=1, rowspan=7, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.canvas = tk.Canvas(board_frame, width=800, height=800, bg='white')
        self.canvas.grid(row=0, column=0)
        
        # Start buttons
        button_frame = ttk.Frame(root, padding="10")
        button_frame.grid(row=2, column=0, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=0, column=0, padx=5)

        self.start_game_button = ttk.Button(button_frame, text="Start Game", command=self.start_game)
        self.start_game_button.grid(row=0, column=1, padx=5)
        
        
    def start_simulation(self):
        self.start_button.config(state='disabled')
        self.results_text.delete(1.0, tk.END)
        threading.Thread(target=self.run_simulation, daemon=True).start()

    def start_game(self):
        self.start_game_button.config(state='disabled')
        self.results_text.delete(1.0, tk.END)
        threading.Thread(target=self.run_game, daemon=True).start()
    
    def run_simulation(self):
        num_players = 4
        num_simulations = 10_000
        results = []
        
        for i in range(num_simulations):
            progress = (i + 1) / num_simulations * 100
            self.progress_var.set(progress)
            self.root.update_idletasks()
            
            result = self.run_game(num_players)
            results.append(result)
        
        self.show_results(results)
        self.start_button.config(state='normal')

    def run_game(self, num_players=4):
        if not self.game:
            self.game = Game(num_players)

        if self.game.is_game_over():
            self.results_text.insert(tk.END, "Game over\n")
            return self.game.game_log
                
        message = self.game.simulate_next_player()
        self.results_text.insert(tk.END, message + "\n")

        self.draw_board(self.game)
        self.start_game_button.config(state='normal')
        self.root.update_idletasks()
        
        return self.game.game_log
    
    def show_results(self, results):
        stats = [
            f"Average turns: {sum(r.num_turns for r in results) / len(results):.2f}",
            f"Max turns: {max(results, key=lambda r: r.num_turns).num_turns}",
            f"Min turns: {min(results, key=lambda r: r.num_turns).num_turns}",
            f"Games with turns over 20: {sum(1 for r in results if r.num_turns >= 20) / len(results) * 100:.2f}%",
            f"Games with turns over 50: {sum(1 for r in results if r.num_turns >= 50) / len(results) * 100:.2f}%",
            f"Games with no winner: {sum(1 for r in results if r.player_id is None) / len(results) * 100:.2f}%",
            f"Player 1 wins: {sum(1 for r in results if r.player_id == 0) / len(results) * 100:.2f}%",
            f"Player 2 wins: {sum(1 for r in results if r.player_id == 1) / len(results) * 100:.2f}%",
            f"Player 3 wins: {sum(1 for r in results if r.player_id == 2) / len(results) * 100:.2f}%",
            f"Player 4 wins: {sum(1 for r in results if r.player_id == 3) / len(results) * 100:.2f}%",
        ]
        
        self.results_text.delete(1.0, tk.END)
        for stat in stats:
            self.results_text.insert(tk.END, stat + "\n")

    def draw_board(self, game=None):
        self.canvas.delete("all")
        
        # Draw the basic board outline
        height = 1000
        width = 1000
        self.canvas.create_rectangle(50, 50, 50 + width, 50 + height, width=2)
        
        # Define space dimensions
        space_size = 100
        
        # Draw corner spaces
        board = self.game.board
        current_x = 650
        current_y = 650
        current_direction = 'left'
        current_space = 0

        for space in board.spaces:
            owner_color = self._find_space_owner(space.owner, game.players)
            self.draw_space(current_x, current_y, space_size, space.name, space.color, owner_color)
            current_space += 1
            if current_direction == 'right':
                if current_space == 7:
                    current_space = 1
                    current_y += space_size
                    current_direction = 'down'
                else:
                    current_x += space_size
            elif current_direction == 'down':
                if current_space == 7:
                    current_space = 1
                    current_x -= space_size
                    current_direction = 'left'
                else:
                    current_y += space_size
            elif current_direction == 'left':
                if current_space == 7:
                    current_space = 1
                    current_y -= space_size
                    current_direction = 'up'
                else:
                    current_x -= space_size
            elif current_direction == 'up':
                if current_space == 7:
                    current_space = 1
                    current_x += space_size
                    current_direction = 'right'
                else:
                    current_y -= space_size
        
        if game:
            self.draw_players(game)

    def draw_space(self, x, y, size, text, color, owner_color):
        self.canvas.create_rectangle(x, y, x + size, y + size, fill=str(color), width=1)
        if text:
            self.canvas.create_text(x + size/2, y + size/2, text=text, width=size-10, fill='black')
        if owner_color:
            self.canvas.create_rectangle(x + 15, y + 15, x + 30, y + 30, fill=str(owner_color), width=1)

    def draw_players(self, game):
        for i, player in enumerate(game.players):
            # Find player position
            space_index = game.board.spaces.index(player.space)
            
            # Calculate position based on space index
            if space_index < 18 and space_index >= 12:  # Top row
                x = 50 + ((space_index % 6) * 100)
                y = 50
            elif space_index > 18:  # Right column
                x = 650
                y = 50 + ((space_index % 6) * 100)
            elif space_index <= 6:  # Bottom row
                x = 650 - (space_index * 100)
                y = 650
            else:  # Left column
                x = 50
                y = 650 - ((space_index % 6) * 100)
            
            # Draw player token
            offset = 30 + (i * 15)
            self.canvas.create_oval(x + offset, y + offset, 
                                  x + offset + 10, y + offset + 10, 
                                  outline=str('black'),
                                  fill=str(player.color))
            
        self.player_1_text.delete(1.0, tk.END)
        self.player_1_text.insert(tk.END, f"Player 1: {game.players[0].color} - ${game.players[0].cash}")
        self.player_2_text.delete(1.0, tk.END)
        self.player_2_text.insert(tk.END, f"Player 2: {game.players[1].color} - ${game.players[1].cash}")
        self.player_3_text.delete(1.0, tk.END)
        self.player_3_text.insert(tk.END, f"Player 3: {game.players[2].color} - ${game.players[2].cash}")
        self.player_4_text.delete(1.0, tk.END)
        self.player_4_text.insert(tk.END, f"Player 4: {game.players[3].color} - ${game.players[3].cash}")

    def _find_space_owner(self, owner, players):
        for player in players:
            if player.id == owner:
                return player.color
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationGUI(root)
    root.mainloop()
