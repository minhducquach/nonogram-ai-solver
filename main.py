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
        self.solver = None
        self.is_solving = False  # Flag to control the solving process
        self.should_stop = False  # Flag to indicate whether the solver should stop
        self.step_solving = False

        self.height = 0
        self.width = 0
        self.cell_size = 75

        self.load_testcase()

        self.canvas = tk.Canvas(self.master, width=self.width*self.cell_size, height=self.height*self.cell_size)
        self.canvas.pack()

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
        f = open(self.testcase, 'r')
        for line in f:
            line_items = line.split(" ")
            self.height = int(line_items[0])
            self.width = int(line_items[1])
            break

    def draw_grid(self):
        self.cells = [[None] * self.width for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.cells[i][j] = self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

    def update_grid(self, grid):
        for i in range(self.height):
            for j in range(self.width):
                cell_color = "black" if grid[i][j] == 1 else "white"
                self.canvas.itemconfig(self.cells[i][j], fill=cell_color)

    def play(self):
        if self.is_solving:
            messagebox.showinfo("Info", "Solver is already running.")
            return
        else:
            self.is_solving = True
            self.should_stop = False
        self.selected_model = self.model_selection.get()
        if self.selected_model == "Blind Search" and self.solver == None:
            self.solver = NonogramBlindSearchSolver(self.testcase)
        elif self.selected_model == "A* Search" and self.solver == None:
            self.solver = NonogramAStarSolver(self.testcase)

        self.is_solving = True
        self.solve_wrapper()

    def solve_wrapper(self):
        self.solver.solve()
        grid = self.solver.grid
        self.update_grid(grid)
        
        if self.solver.goalFlag:
            messagebox.showinfo("Info", "Goal state reached.")
            self.should_stop = True
            self.is_solving = False
            self.self_solving = False

            self.play_button["state"] = "disabled"
            self.pause_button["state"] = "disabled"
            self.step_button["state"] = "disabled"
            return
        # Check if solving should continue
        if not self.should_stop:
            self.master.after(100, self.solve_wrapper)

    def pause(self):
        if not self.is_solving:
            messagebox.showinfo("Info", "Solver is not running.")
            return
        self.should_stop = True
        self.is_solving = False
        if not self.step_solving:
            messagebox.showinfo("Info", "Solver paused.")
        else:
            self.step_solving = False

    def step_by_step(self):
        if self.is_solving:
            messagebox.showinfo("Info", "Solver is already running.")
            return
        else:
            self.is_solving = True
            self.step_solving = True
        self.selected_model = self.model_selection.get()
        if self.selected_model == "Blind Search" and self.solver == None:
            self.solver = NonogramBlindSearchSolver(self.testcase)
        elif self.selected_model == "A* Search" and self.solver == None:
            self.solver = NonogramAStarSolver(self.testcase)

        self.solver.solve()
        grid = self.solver.grid
        self.update_grid(grid)
        
        if self.solver.goalFlag:
            messagebox.showinfo("Info", "Goal state reached.")
            self.should_stop = True
            self.is_solving = False
            self.self_solving = False

            self.play_button["state"] = "disabled"
            self.pause_button["state"] = "disabled"
            self.step_button["state"] = "disabled"
            return
        self.pause()

def main():
    root = tk.Tk()
    app = NonogramApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
