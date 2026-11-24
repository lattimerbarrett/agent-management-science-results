# Central characters distinguish PGL-linearizability from invariance.
# O(k) is invariant under PGL_{n+1}; its usual SL_{n+1}
# linearization descends to PGL precisely when n+1 divides k.
for n in range(2, 6):
    k = 1
    print(f'P^{n}: O(1) is invariant; SL central weight mod {n+1} = {(-k) % (n+1)}, so not PGL-linearizable.')
