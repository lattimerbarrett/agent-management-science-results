# Bookkeeping for the arithmetical-hierarchy exclusions.
# Verified mathematical inputs:
# (1) Every Sigma^0_2 set has a total skip.
# (2) Every Pi^0_2 set has a cototal skip.
# Membership in lower levels embeds in the same-label higher levels,
# and in the opposite-label level one step higher.
labels = ('Sigma', 'Pi')
excluded = {(label, m) for label in labels for m in (1, 2)}
print('Excluded:', sorted(excluded))
print('Not settled by these exclusions:', [(label, m) for m in range(3, 7) for label in labels])
print('No higher-complexity existence assertion has been established.')
