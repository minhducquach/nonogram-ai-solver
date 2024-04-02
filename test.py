# import numpy as np
# from itertools import combinations

# A = np.zeros((15), dtype=int)
# B = np.array([3,2,6])

# opts = combinations(range(3+2), 3)
# res = []
# for p in opts:
#     print(p)
#     res_opt = []
#     for i in range(len(p)):
#         if i == 0 and p[i] != 0:
#             res_opt += [0]*p[i]
#             res_opt += [1]*B[i]
#         elif i == 0 and p[i] == 0:
#             res_opt += [1]*B[i]
#         elif i != 0:
#             res_opt += [0]*(p[i]-p[i-1])
#             res_opt += [1]*B[i]
#     if len(res_opt) < A.shape[0]:
#         res_opt += [0]*(A.shape[0] - len(res_opt))
#     print(res_opt)

# A = [1,2,3,4,5]
# B = [1,6,5,2,4]
# B = A
# B[0] = 2
# print("A:", A)
# print("B:", B)

import numpy as np

def check_column_constraints(board):
    """
    Checks if the nonogram board satisfies all column constraints.

    Args:
        board (np.ndarray): 2D numpy array representing the nonogram board.

    Returns:
        bool: True if all column constraints are satisfied, False otherwise.
    """
    num_rows, num_cols = board.shape

    # Iterate over each column
    for col in range(num_cols):
        column = board[:, col]
        constraints = []

        # Initialize the current constraint
        current_constraint = 0

        # Iterate over each cell in the column
        for cell in column:
            if cell == 1:
                # If cell is filled, increment the current constraint
                current_constraint += 1
            elif current_constraint > 0:
                # If cell is empty and there was a previous constraint, add it to the list
                constraints.append(current_constraint)
                current_constraint = 0

        # If there's a current constraint at the end, add it to the list
        if current_constraint > 0:
            constraints.append(current_constraint)

        # Compare the constraints with the column constraints
        if tuple(constraints) != tuple(column_constraints[col]):
            return False

    return True

# Example usage
# Define the nonogram board (0 for empty, 1 for filled)
nonogram_board = np.array([[1, 0, 1],
                           [0, 1, 0],
                           [1, 0, 1]])

# Define the column constraints (e.g., [1, 1] means one filled cell followed by one empty cell)
column_constraints = [[1, 1], [1], [1, 1]]

# Check if the board satisfies all column constraints
result = check_column_constraints(nonogram_board)
print(f"Column constraints satisfied: {result}")
