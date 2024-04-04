import numpy as np
from copy import deepcopy
from itertools import combinations
from queue import PriorityQueue

class NonogramAStarSolver:
    def __init__(self, testcase):
        self.step_count = 0
        self.height = 0
        self.width = 0
        self.grid = None
        self.state_queue = PriorityQueue()
        self.state_stack = []
        self.row_constraints = []
        self.col_constraints = []
        self.possibleRowForms = []
        self.possibleColForms = []
        self.initializeGrid(testcase)
        self.generatePossibleRowForms()
        self.generatePossibleColForms()
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
                self.row_constraints.append(row)
            else:
                col = []
                for i in line_items:
                    col.append(int(i))
                self.col_constraints.append(col)
            count_line += 1
    
    def generatePossibleRowForms(self):
        for row_constraint in self.row_constraints:
            res = []
            num_groups = len(row_constraint)
            num_empty = self.width - sum(row_constraint) - num_groups + 1
            options = combinations(range(num_groups + num_empty), num_groups)
            for opt in options:
                res_opt = []
                for i in range(len(opt)):
                    if i == 0 and opt[i] != 0:
                        res_opt += [0] * opt[i]
                        res_opt += [1] * row_constraint[i]
                    elif i == 0 and opt[i] == 0:
                        res_opt += [1] * row_constraint[i]
                    elif i != 0:
                        res_opt += [0] * (opt[i] - opt[i-1])
                        res_opt += [1] * row_constraint[i]
                if len(res_opt) < self.width:
                    res_opt += [0] * (self.width - len(res_opt))
                res_opt = np.array(res_opt, dtype=int)
                res.append(res_opt)
            self.possibleRowForms.append(res)
        # print("POS:", self.possibleRowForms[0])
    
    def generatePossibleColForms(self):
        for col_constraint in self.col_constraints:
            res = []
            num_groups = len(col_constraint)
            num_empty = self.height - sum(col_constraint) - num_groups + 1
            options = combinations(range(num_groups + num_empty), num_groups)
            for opt in options:
                res_opt = []
                for i in range(len(opt)):
                    if i == 0 and opt[i] != 0:
                        res_opt += [0] * opt[i]
                        res_opt += [1] * col_constraint[i]
                    elif i == 0 and opt[i] == 0:
                        res_opt += [1] * col_constraint[i]
                    elif i != 0:
                        res_opt += [0] * (opt[i] - opt[i-1])
                        res_opt += [1] * col_constraint[i]
                if len(res_opt) < self.height:
                    res_opt += [0] * (self.height - len(res_opt))
                res_opt = np.array(res_opt, dtype=int)
                res.append(res_opt)
            self.possibleColForms.append(res)
        print("POS:", self.possibleColForms)

    def printState(self, isGoalFlag = 0):
        if isGoalFlag != 1:
            if self.step_count == 0:
                print("Initial state:")
            else:
                print(f'State {self.step_count}:')
        else:
            print("Goal state:")
        for row in self.grid:
            print(" | ".join(map(str, row)))
        self.step_count += 1

    def assembleStateGrid(self, state):
        for i in range(self.height):
            if state[i] == 0:
                self.grid[i] = np.zeros((self.width), dtype=int)
            else:
                self.grid[i] = self.possibleRowForms[i][state[i]-1]
        return

    def checkColConstraints(self):
        for col in range(self.width):
            column = self.grid[:,col]
            constraint_check = []
            current = 0
            for cell in column:
                if cell == 1:
                    current += 1
                else:
                    if current != 0:
                        constraint_check.append(current)
                    current = 0
            if current > 0:
                constraint_check.append(current)
            print(f'COUNT COL {col}: {constraint_check} vs CONSTRAINT COL {col}: {self.col_constraints[col]}')
            if constraint_check != self.col_constraints[col]:
                print(f'COL {col} WRONG')
                return False
        print(f'ALL COLS CORRECT!')
        return True

    def isGoal(self, state):
        # assemble grid, check, print, return flag
        if self.step_count == 1:
            self.printState()
            return False
        self.assembleStateGrid(state)
        if self.checkColConstraints():
            self.printState(isGoalFlag = 1)
            return True
        self.printState()
        return False

    def checkLeaf(self, state):
        for i, val in enumerate(state):
            if val == 0:
                return i
        return -1

    def solve(self):
        state = [0] * self.height
        self.state_queue.put((0, state))
        while not self.state_queue.empty():
            _, state = self.state_queue.get()
            if self.isGoal(state):
                return
            index = self.checkLeaf(state)
            if index != -1:
                for i in range(1,len(self.possibleRowForms[index])+1):
                    child_state = deepcopy(state)
                    child_state[index] += i
                    priority = self.calculateCost(child_state)
                    self.state_queue.put((priority, child_state))
    
    def calculateCost(self, state):
        cost = 0
        self.assembleStateGrid(state)
        # For each row and column, check if it satisfies the constraints, if not, add 1 to the cost
        for i in range(self.height):
            if not np.array_equal(self.grid[i], self.possibleRowForms[i][state[i]-1]):
                cost += 1
        for j in range(self.width):
            column = self.grid[:,j]
            for k in range(len(self.possibleColForms[j])):
                if not np.array_equal(column, self.possibleColForms[j][k]):
                    cost += 1
        return cost
    
if __name__ == '__main__':
    problem = NonogramAStarSolver(testcase = './testcase.txt')
    problem.solve()