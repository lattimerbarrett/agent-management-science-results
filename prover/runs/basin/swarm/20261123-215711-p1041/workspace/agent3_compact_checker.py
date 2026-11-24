from collections import Counter
TABLE = [([127, 1927, 6203], 127), ([127, 8065, 926], 8423), ([127, 1927, 16256], 14729), ([127, 3971, 14212], 127), ([127, 911, 2032], 15505), ([127, 415, 15968], 4001), ([127, 415, 1955], 4004), ([127, 415, 15968], 15875), ([127, 415, 15968], 1927), ([127, 911, 7569], 8080), ([127, 415, 15968], 3683), ([127, 1927, 16256], 2297), ([127, 191, 1863], 127)]
# Each mask M denotes the coordinate 7-space {x:x&~M=0}.
def flat(M):
 assert M.bit_count()==7
 return {x for x in range(16384) if x & (16383 ^ M)==0}
covered=0
for masks,Q in TABLE:
 assert Q.bit_count()==7
 S=flat(masks[0])^flat(masks[1])^flat(masks[2])
 counts=Counter(x&Q for x in S)
 occupancies=list(counts.values())+[0]*(128-len(counts))
 assert len(occupancies)==128 and sum(occupancies)==len(S)
 # Choose independently either S or its complement in each Q-coset.
 base=sum(min(n,128-n) for n in occupancies)
 bits=1
 for n in occupancies:bits |= bits<<abs(128-2*n)
 covered |= bits<<base
missing=[w for w in range(336,8193,2) if not((covered>>w)&1)]
assert missing==[358,362],missing
print('13 explicit coset-switch families cover every even weight 336..8192 except 358,362')
