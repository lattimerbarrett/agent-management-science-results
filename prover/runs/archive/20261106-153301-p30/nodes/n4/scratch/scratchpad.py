from itertools import product
# Six disjoint moment-curve intervals. Each minimal four-region traversal
# has cut-label word ABA or BAB. Test degree bounds d=9.
valid=[]
for blocks in product(('ABA','BAB'), repeat=6):
    word=''.join(blocks)
    if word.count('A')<=9 and word.count('B')<=9:
        valid.append(blocks)
print('Feasible minimal-cut block assignments:',len(valid))
print('Example:', valid[0])
# Track actual sign regions (A,B sign bits) across each interval.
state=(0,0)
for block in valid[0]:
    regions=[state]
    for letter in block:
        state=(1-state[0],state[1]) if letter=='A' else (state[0],1-state[1])
        regions.append(state)
    print(block, regions, 'visits all four:', len(set(regions))==4)
