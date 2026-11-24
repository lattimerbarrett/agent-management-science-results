# Propagate the verified Pi_2 existence result through the
# parameter-free arithmetical hierarchy (up to a displayed cutoff).
N = 8
witness_levels = {('Pi', m) for m in range(2, N+1)} | {('Sigma', m) for m in range(3, N+1)}
excluded_levels = {('Sigma', 1), ('Sigma', 2), ('Pi', 1)}
all_levels = {(s,m) for s in ('Sigma','Pi') for m in range(1,N+1)}
assert not (witness_levels & excluded_levels)
assert witness_levels | excluded_levels == all_levels
for s in ('Sigma', 'Pi'):
    print(s, sorted(m for label,m in witness_levels if label == s))
print('All levels accounted for:', witness_levels | excluded_levels == all_levels)
