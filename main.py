import numpy as np
from itertools import combinations

class NonogramSolver:
    def __init__(self, testcase):
        self.step_count = 0
        self.height = 0
        self.width = 0
        self.grid = None
        self.row_values = []
        self.col_values = []
        self.possibleRowForms = []
        self.initializeGrid(testcase)
        self.generatePossibleRowForms()
        self.printState()

    def initializeGrid(self, testcase):
        count_line = 0
        f = open(testcase, 'r')
        for line in f:
            line_items = line.split(" ")
            if (count_line == 0):
                self.height = int(line_items[0])
                self.width = int(line_items[1])
                self.grid = np.zeros((self.height, self.width), dtype=int)
            elif (count_line <= self.height):
                row = []
                for i in line_items:
                    row.append(int(i))
                self.row_values.append(row)
            else:
                col = []
                for i in line_items:
                    col.append(int(i))
                self.col_values.append(col)
            count_line += 1
    
    def generatePossibleRowForms(self):
        for row_val in self.row_values:
            res = []
            num_groups = len(row_val)
            num_empty = len(self.col_values) - sum(row_val) - num_groups + 1
            options = combinations(range(num_groups + num_empty), num_groups)
            for opt in options:
                res_opt = []
                for i in range(len(opt)):
                    if i == 0 and opt[i] != 0:
                        res_opt += [0] * opt[i]
                        res_opt += [1] * row_val[i]
                    elif i == 0 and opt[i] == 0:
                        res_opt += [1] * row_val[i]
                    elif i != 0:
                        res_opt += [0] * (opt[i] - opt[i-1])
                        res_opt += [1] * row_val[i]
                if len(res_opt) < len(self.col_values):
                    res_opt += [0] * (len(self.col_values) - len(res_opt))
                res.append(res_opt)
            self.possibleRowForms.append(res)

    def printState(self):
        if self.step_count == 0:
            print("Initial state:")
        else:
            print(f'Step {self.step_count}:')
        for row in self.grid:
            print(" | ".join(map(str, row)))

    # def checkRowConstraints(self):
    #     pass
    def isGoal(self):
        pass

    def checkColConstraints(self):
        pass

    def solveBlindSearch(self):
        print("SOLVED")


if __name__ == '__main__':
    problem = NonogramSolver(testcase = './testcase.txt')
    problem.solveBlindSearch()