from itertools import product, combinations

def plane(q):
    pts=[]
    for v in product(range(q), repeat=3):
        if not any(v): continue
        a=next(x for x in v if x)
        w=tuple((x*pow(a,-1,q))%q for x in v)
        if w not in pts: pts.append(w)
    lines=[]
    for a in pts:
        lines.append(frozenset(i for i,p in enumerate(pts) if sum(x*y for x,y in zip(a,p))%q==0))
    return pts,lines

# Check the natural construction: core at point i, with remainder L\{i}
# for each incident line. Each core contains the representative of its point.
# Private padding does not improve on these representatives in a transversal.
for q in [2,3,5]:
    pts, lines=plane(q)
    tau=None
    for s in range(q+2):
        if any(all(set(C)&L for L in lines) for C in combinations(range(len(pts)),s)):
            tau=s; break
    print({'q':q,'groups':len(pts),'remainder_size':q,'actual_covering_number':tau})
