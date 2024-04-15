import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from blindSearchSolver import NonogramBlindSearchSolver
from heuristicSolver import NonogramAStarSolver
import threading

class NonogramApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Nonogram Solver")

        self.selected_model = None
        self.is_solving = False  # Flag to control the solving process
        self.should_stop = False  # Flag to indicate whether the solver should stop

        self.grid_size = 8
        self.cell_size = 50

        self.canvas = tk.Canvas(self.master, width=self.grid_size*self.cell_size, height=self.grid_size*self.cell_size)
        self.canvas.pack()

        self.load_testcase()
        self.draw_grid()

        self.play_button = tk.Button(self.master, text="Play", command=self.play)
        self.play_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(self.master, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT)

        self.step_button = tk.Button(self.master, text="Step by Step", command=self.step_by_step)
        self.step_button.pack(side=tk.LEFT)

        self.model_selection = tk.StringVar()
        self.model_selection.set("Blind Search")  # Default selection
        self.blind_search_radio = tk.Radiobutton(self.master, text="Blind Search", variable=self.model_selection, value="Blind Search")
        self.blind_search_radio.pack(side=tk.RIGHT)

        self.a_star_radio = tk.Radiobutton(self.master, text="A* Search", variable=self.model_selection, value="A* Search")
        self.a_star_radio.pack(side=tk.RIGHT)

    def load_testcase(self):
        # Load your test case here
        self.testcase = './testcase.txt'

    def draw_grid(self):
        self.cells = [[None] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.cells[i][j] = self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

    def update_grid(self, grid):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell_color = "black" if grid[i][j] == 1 else "white"
                self.canvas.itemconfig(self.cells[i][j], fill=cell_color)

    def play(self):
        if self.is_solving:
            messagebox.showinfo("Info", "Solver is already running.")
            return

        self.selected_model = self.model_selection.get()
        if self.selected_model == "Blind Search":
            self.solver = NonogramBlindSearchSolver(self.testcase)
        elif self.selected_model == "A* Search":
            self.solver = NonogramAStarSolver(self.testcase)

        self.is_solving = True
        thread = threading.Thread(target=self.solve_wrapper)
        thread.start()

    def solve_wrapper(self):
        if self.selected_model == "Blind Search":
            self.solver.solveDFS()
        elif self.selected_model == "A* Search":
            self.solver.solve()
        
       
        grid = self.solver.grid
        
       
        self.update_grid(grid)
        
        # Check if solving should continue
        if not self.should_stop:
           
            self.master.after(1000, self.solve_wrapper)

    def pause(self):
        if not self.is_solving:
            messagebox.showinfo("Info", "Solver is not running.")
            return
        self.should_stop = True
        messagebox.showinfo("Info", "Solver paused.")

    def step_by_step(self):
        if not self.selected_model:
            messagebox.showinfo("Error", "Please select a model first.")
            return

        if not self.is_solving:
            self.is_solving = True

            if self.selected_model == "Blind Search":
                self.solver.solveDFS()
            elif self.selected_model == "A* Search":
                self.solver.solve()

            self.is_solving = False
            self.update_grid(self.solver.grid)

def main():
    root = tk.Tk()
    app = NonogramApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
