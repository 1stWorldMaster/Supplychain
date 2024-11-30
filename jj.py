import ortools
from ortools.linear_solver import pywraplp
import threading
import multiprocessing
import numpy as np
def solve_packing(items, box_length, box_width, box_height, box_weight_limit):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("SCIP solver not found!")
        return None
    
    n = len(items)
    S = []
    for i in range(n):
        S.append(solver.BoolVar(f"S_{i}"))
    
    X_coordinates = []
    Y_coordinates = []
    Z_coordinates = []
    X_r_coordinates = []
    Y_r_coordinates = []
    Z_r_coordinates = []
    rotation_matrix = []

    for i in range(n):
        X_coordinates.append(solver.IntVar(0, box_length, f"X_{i}"))
        Y_coordinates.append(solver.IntVar(0, box_width, f"Y_{i}"))
        Z_coordinates.append(solver.IntVar(0, box_height, f"Z_{i}"))
        X_r_coordinates.append(solver.IntVar(0, box_length, f"X_r_{i}"))
        Y_r_coordinates.append(solver.IntVar(0, box_width, f"Y_r_{i}"))
        Z_r_coordinates.append(solver.IntVar(0, box_height, f"Z_r_{i}"))
        
        # Create rotation matrix variables
        vector = []
        for j in range(3):
            for k in range(3):
                vector.append(solver.BoolVar(f"t_{i}{j}{k}"))
        rotation_matrix.append(vector)
        
        # Add rotation matrix constraints
        for j in range(3):
            # Each row and column must sum to S[i] (1 if selected, 0 if not)
            solver.Add(sum(rotation_matrix[i][j*3 + k] for k in range(3)) == S[i])
            solver.Add(sum(rotation_matrix[i][k*3 + j] for k in range(3)) == S[i])
        
        # Link coordinates with rotation and selection
        solver.Add(X_r_coordinates[i] == X_coordinates[i] + 
                  rotation_matrix[i][0]*items[i][0] + 
                  rotation_matrix[i][1]*items[i][1] + 
                  rotation_matrix[i][2]*items[i][2])
        
        solver.Add(Y_r_coordinates[i] == Y_coordinates[i] + 
                  rotation_matrix[i][3]*items[i][0] + 
                  rotation_matrix[i][4]*items[i][1] + 
                  rotation_matrix[i][5]*items[i][2])
        
        solver.Add(Z_r_coordinates[i] == Z_coordinates[i] + 
                  rotation_matrix[i][6]*items[i][0] + 
                  rotation_matrix[i][7]*items[i][1] + 
                  rotation_matrix[i][8]*items[i][2])
        
        # Box boundary constraints
        solver.Add(X_r_coordinates[i] <= box_length * S[i])
        solver.Add(Y_r_coordinates[i] <= box_width * S[i])
        solver.Add(Z_r_coordinates[i] <= box_height * S[i])

    L=[[None for i in range(n)] for j in range(n)]
    R=[[None for i in range(n)] for j in range(n)]
    F=[[None for i in range(n)] for j in range(n)]
    B=[[None for i in range(n)] for j in range(n)]
    U=[[None for i in range(n)] for j in range(n)]
    O=[[None for i in range(n)] for j in range(n)]

    # Non-overlapping constraints
    for i in range(n):
        for j in range(i+1, n):
            # Create separation variables
            L[i][j]=solver.BoolVar(f"L_{i}_{j}")
            R[i][j]=solver.BoolVar(f"R_{i}_{j}")
            F[i][j]=solver.BoolVar(f"F_{i}_{j}")
            B[i][j]=solver.BoolVar(f"B_{i}_{j}")
            U[i][j]=solver.BoolVar(f"U_{i}_{j}")
            O[i][j]=solver.BoolVar(f"O_{i}_{j}")
            
            # If both items are selected, they must be separated in at least one dimension
            solver.Add(L[i][j] + R[i][j] + F[i][j] + B[i][j] + U[i][j] + O[i][j] >= S[i] + S[j] - 1)
            
            # Position constraints
            solver.Add(X_r_coordinates[i] <= X_coordinates[j] + box_length * (1 - L[i][j]))
            solver.Add(X_r_coordinates[j] <= X_coordinates[i] + box_length * (1 - R[i][j]))
            solver.Add(Y_r_coordinates[i] <= Y_coordinates[j] + box_width * (1 - F[i][j]))
            solver.Add(Y_r_coordinates[j] <= Y_coordinates[i] + box_width * (1 - B[i][j]))
            solver.Add(Z_r_coordinates[i] <= Z_coordinates[j] + box_height * (1 - U[i][j]))
            solver.Add(Z_r_coordinates[j] <= Z_coordinates[i] + box_height * (1 - O[i][j]))

    # Weight constraint
    solver.Add(solver.Sum(S[i]*items[i][3] for i in range(n)) <= box_weight_limit)
    
    # Objective
    solver.Maximize(solver.Sum(S[i] for i in range(n)))

    status=solver.Solve()

    if (status == pywraplp.Solver.OPTIMAL):
        for i in range(n):
          if S[i].solution_value() == 1:
            print(f"Item {i}:")
            print(f"Position: ({X_coordinates[i].solution_value()}, {Y_coordinates[i].solution_value()}, {Z_coordinates[i].solution_value()})")
            print(f"End position: ({X_r_coordinates[i].solution_value()}, {Y_r_coordinates[i].solution_value()}, {Z_r_coordinates[i].solution_value()})")

    else:
        print("No solution found.")
      
def main():
  items = [
    (60, 50, 40, 85),
    (70, 50, 30, 90),
    (30, 20, 20, 30),
    (50, 40, 30, 70),
    (80, 60, 40, 100),
    (90, 50, 50, 120),
    (20, 20, 10, 20),
    (10, 70, 50, 130),
    (40, 30, 20, 40),
    (60, 50, 30, 60),
    (10, 10, 10, 10),
    (50, 30, 40, 70),
    (70, 60, 50, 110),
    (40, 40, 30, 50),
    (80, 70, 60, 30),
    (30, 20, 10, 30),
    (50, 50, 40, 80),
    (90, 40, 60, 20),
    (20, 20, 30, 40),
    (40, 30, 30, 50),
    (60, 40, 30, 70),
    (70, 60, 40, 100),
    (20, 10, 10, 20),
    (40, 30, 40, 80),
    (60, 50, 40, 85),
    (70, 50, 30, 90),
    (30, 20, 20, 30),
    (50, 40, 30, 70),
    (80, 60, 40, 100),
    (90, 50, 50, 120),
    (20, 20, 10, 20),
    (10, 70, 50, 130),
    (40, 30, 20, 40),
    (60, 50, 30, 60),
    (200,180,240,100)
  ]

  box=[200,180,240,3000]
  solve_packing(items, box[0], box[1], box[2], box[3])


main()