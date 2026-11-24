# Check the elementary central-character distinction discussed above.
# The central element zeta*I in SL(N) acts on O(k)'s fiber by zeta^(-k).
# It acts trivially for every zeta^N=1 exactly when N divides k.
for N in (3, 4, 5):
    print({'projective_dimension': N - 1,
           'O(1)_SL_equivariant': True,
           'O(1)_PGL_descent': (1 % N == 0)})
