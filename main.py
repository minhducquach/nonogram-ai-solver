# main.py
from blindSearchSolver import NonogramBlindSearchSolver
from heuristicSolver import NonogramAStarSolver
import numpy as np

def print_nonogram(grid):
    for row in grid:
        row_str = ''.join('█' if cell == 1 else ' ' for cell in row)
        print(row_str)

def main():
    # Replace './testcase.txt' with the path to your test case file
    test_case_path = './testcase.txt'

    # Initialize the blind search solver
    blind_solver = NonogramBlindSearchSolver(test_case_path)

    # Initialize the heuristic solver
    heuristic_solver = NonogramAStarSolver(test_case_path)

    # Solve with blind search solver
    blind_solution = blind_solver.solve()

    # Solve with heuristic solver
    heuristic_solution = heuristic_solver.solve()

    # Convert solutions to Nonogram table
    blind_grid = np.array([blind_solver.possibleRowForms[i][val - 1] for i, val in enumerate(blind_solution)])
    heuristic_grid = np.array([heuristic_solver.possibleRowForms[i][val - 1] for i, val in enumerate(heuristic_solution)])

    # Print Nonogram grids
    print("Blind Search Solver Solution:")
    print_nonogram(blind_grid)
    print("\nHeuristic Solver Solution:")
    print_nonogram(heuristic_grid)

if __name__ == '__main__':
    main()
