# Rigorous exclusion of all degrees d>=7 for even n>=10
Let G be connected, simple and dregular, not complete. Unit resistances throughout.

## Two adjacent-edge lower bounds
For every edge uv, R_uv>=r0=2/(d+1), by contracting all other vertices to one vertex.
Call uv a twin edge if N[u]=N[v]. For a nontwin edge choose distinct w in N(u)\N[v], z in N(v)\N[u]; existence of both follows regularity. Test the Dirichlet variational principle R_uv>= (f(u)-f(v))^2/E(f) with f(u)=1,f(v)=-1,f(w)=epsilon,f(z)=-epsilon and all other potentials zero. The diagonal and offdiagonal terms give
E(f)=2(d+1)-4epsilon+2(d+1_{wz in E})epsilon^2
<=2(d+1)-4epsilon+2(d+1)epsilon^2.
Set epsilon=1/(d+1), to obtain R_uv>=r1=2(d+1)/[d(d+2)]. Thus g=r1-r0=2/[d(d+1)(d+2)].

## At least 3n/2 nontwin edges when d>=5
Closed-neighborhood twin equivalence classes are cliques. If one has size a, every vertex in it has external degree d+1-a. No class can have size d or d+1: in either case its vertices and their remaining neighbor(s) form an isolated K_{d+1}, contrary to connected noncompleteness. Hence every external degree is >=2.
Let A be the set of vertices with external degree2; each such class has size d-1. Each vertex x outside such a class adjacent to it is adjacent to its d-1 members. It must be a singleton twin class: a twin y of x would, with the d-1 class members, form a complete K_{d+1} component. Let B consist of all these outside neighbors. Each B vertex has external degree d and is adjacent to exactly d-1 vertices of A, because it cannot touch two disjoint classes of size d-1. Consequently (d-1)|B|=2|A|. Every remaining vertex C has external degree>=3. Thus twice the number of nontwin edges is at least
2|A|+d|B|+3|C|=3n+(d-5)|A|/(d-1)>=3n.

## Foster + shortest path
Foster gives sum_e R_e=n-1. If P is a shortest u-v path of length l, the resistance triangle inequality and the edge lower bounds imply
R_uv<=sum_{e in P}R_e
<=n-1-(dn/2-l)r0-(3n/2-l)g.
This uses 3n/2-l>=0, which holds as l<=n-1. Closed neighborhoods of the vertices at path positions0,3,6,... are disjoint, so floor(l/3)+1<=n/(d+1). Hence l<=3n/(d+1)-1.
Substitution and simplification give
 dR_uv <= [(d^2+8d+3)/((d+1)(d+2))] n -d-2+2/(d+2).
For d>=7, the coefficient is <=3/2, since their difference is d(d-7)/[2(d+1)(d+2)]. The constant is at most its d7 value -79/9<-33/4. Thus
 dR_uv < 3n/2-33/4,
below both even-n target normalized resistances.
If G is complete, R=2/n and dR<2, also trivially below the target for n>=10.
The commute is ndR, giving the desired exclusion of every d>=7.
