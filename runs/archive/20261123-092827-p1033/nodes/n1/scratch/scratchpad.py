from itertools import combinations
for t in range(2,9):
    # A set hits all of class i iff it meets X_i or contains some X_j, j<i.
    # Optimize over occupancy counts; without a full block all t blocks must be hit.
    # If j is the first full block, earlier blocks must be hit, later need not be.
    candidates=[t]+[(j-1)+(t-j+1) for j in range(1,t+1)]
    print(t, min(candidates))
