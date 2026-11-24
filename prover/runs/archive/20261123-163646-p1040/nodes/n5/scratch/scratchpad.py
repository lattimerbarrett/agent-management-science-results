# Verify the strong-centrality condition in the illustrative filtrations.
# In a class-d group C_r denotes gamma_r(G), with C_{d+1}=1.
# A_r = C_{s(r)}. It suffices that s(i)+s(j) >= s(i+j),
# since [C_a,C_b] <= C_{a+b}.
for d in range(1, 7):
    def s(r):
        return min(r, d) if r <= 7 else d+1
    assert all(min(s(i)+s(j), d+1) >= s(i+j)
               for i in range(1, 17) for j in range(1, 17))
print('Verified strong centrality for all six illustrative filtrations.')
print('This verifies only the logical countermodels; it does not compute any IA_n kernel.')