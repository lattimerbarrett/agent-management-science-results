from itertools import combinations
import z3

def check(n,r,t):
 Q=[1<<i for i in range(n)]+[(1<<i)|(1<<j) for i,j in combinations(range(n),2)]
 els=[(p,a) for p in range(1<<r) for a in Q];N=len(els)
 le=[[p&q==p and a&b==a for q,b in els] for p,a in els]
 cp=[(x,y) for x in range(N) for y in range(N) if not le[x][y] and not le[y][x] and all(not(le[z][x] and z!=x) or le[z][y] for z in range(N)) and all(not(le[y][z] and z!=y) or le[x][z] for z in range(N))]
 edges=[(i,j) for i,j in combinations(range(len(cp)),2) if le[cp[i][0]][cp[j][1]] and le[cp[j][0]][cp[i][1]]]
 s=z3.Solver();cs=[z3.Int('c'+str(i)) for i in range(len(cp))]
 s.add(*[z3.And(c>=0,c<t) for c in cs]);s.add(*[cs[i]!=cs[j] for i,j in edges]);s.set(timeout=30000)
 print(n,r,t,len(cp),len(edges),s.check(),flush=True)
if __name__=='__main__':
 for n,t in [(3,3),(4,3),(5,4),(4,4),(5,5)]:check(n,3,t)
