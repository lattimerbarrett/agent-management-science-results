# Check only the hierarchy bookkeeping, not the recursion-theoretic theorems.
# Inputs being considered:
# (1) No Pi^0_2 set is a witness.
# (2) A Delta^0_3 witness is available.
# Sigma^0_1, Pi^0_1, and Sigma^0_2 are all contained in Pi^0_2.
excluded = {('Sigma', 1), ('Pi', 1), ('Sigma', 2), ('Pi', 2)}
# Delta^0_3 is contained in both Sigma^0_m and Pi^0_m for every m >= 3.
for m in range(1, 7):
    print(m, {label: ('excluded' if (label,m) in excluded else 'included if the Delta^0_3 construction applies')
              for label in ('Sigma','Pi')})
