# Check the purely logical induction, without any rank-three numerical input.
# If A_c = gamma_c and the intersection kernel at c vanishes, then
# A_(c+1) = gamma_c intersect A_(c+1) = gamma_(c+1).
for c in range(1, 5):
    print(f'A_{c}=gamma_{c} and K_{c}=0 imply A_{c+1}=gamma_{c+1}')
print('A numerical counterexample can identify a specific kernel degree only after its exact quotient, indexing, and placement in the lower central series are established.')