# Verify the elementary central-character obstruction discussed above.
# The SL(n+1) linearization on O(k) descends to PGL(n+1)
# precisely when the center acts trivially, i.e. (n+1) divides k.
for n in range(2, 6):
    print({'n': n, 'O(1)_PGL_linearizable': (1 % (n+1) == 0),
           'O(n+1)_PGL_linearizable': ((n+1) % (n+1) == 0)})
