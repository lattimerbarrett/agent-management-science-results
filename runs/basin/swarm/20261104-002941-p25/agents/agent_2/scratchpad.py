import itertools, os
import numpy as np
from scipy.sparse import csr_matrix

MODULE = r'''"""Explicit lower-bound construction and exact finite-instance checks."""
import itertools
import numpy as np
from scipy.sparse import csr_matrix

def kneser(m,r):
    sets=list(map(frozenset,itertools.combinations(range(m),r)))
    edges=[(u,v) for u in range(len(sets)) for v in range(u+1,len(sets)) if sets[u].isdisjoint(sets[v])]
    return sets,edges

def construct(m,r,q=1):
    """W_i has m*q vertices, P_i has r*q; skeleton 3-subdivides KG(m,r)."""
    sets,edges=kneser(m,r)
    return construct_from_labels(sets,edges,m,r,q)

def construct_from_labels(sets,edges,m,r,q=1):
    assert all(len(s)==r for s in sets)
    assert all(set(sets[u]).isdisjoint(sets[v]) for u,v in edges)
    types=[0]*len(sets)
    labels=list(sets)
    skeleton=[]
    for u,v in edges:
        a=len(types); b=a+1
        types.extend([1,2]); labels.extend([sets[v],sets[u]])
        skeleton.extend([(u,a),(a,b),(b,v)])
    core_n=len(types)
    adj=[set() for _ in range(core_n)]
    def vertex():
        adj.append(set()); return len(adj)-1
    def add(u,v):
        assert u!=v
        adj[u].add(v); adj[v].add(u)
    for u,v in skeleton: add(u,v)
    for i in range(3):
        W=[[vertex() for _ in range(q)] for j in range(m)]
        P=[vertex() for _ in range(r*q)]
        for cell in W:
            for w in cell:
                for p in P: add(w,p)
        for x in range(core_n):
            if types[x]==i:
                for j in labels[x]:
                    for w in W[j]: add(x,w)
    return adj, dict(m=m,r=r,q=q,core_n=core_n,types=types,labels=labels,skeleton=skeleton,branch_n=len(sets),F_edges=edges)

def check_symbolic_core(data):
    n=data['core_n']; adj=[set() for _ in range(n)]
    for u,v in data['skeleton']: adj[u].add(v);adj[v].add(u)
    count=0
    for a in range(n):
        for b in adj[a]:
            for c in adj[b]:
                for d in adj[c]:
                    if data['types'][a]==data['types'][d]:
                        assert data['labels'][a].isdisjoint(data['labels'][d])
                        count+=1
    for u,v in data['F_edges']:
        assert any(v in adj[b] for a in adj[u] for b in adj[a])
    return count

def check_no_C3_C5(adj):
    n=len(adj)
    rows=[];cols=[]
    for u in range(n):
        for v in adj[u]: rows.append(u);cols.append(v)
    A=csr_matrix((np.ones(len(rows),dtype=np.int64),(rows,cols)),shape=(n,n))
    A2=A@A; A3=A2@A
    # trace(A^3) and trace(A^5) count all closed odd walks, not just induced cycles.
    t3=int(A.multiply(A2).sum())
    t5=int(A2.multiply(A3).sum())
    assert t3==0 and t5==0,(t3,t5)
    return t3,t5

def verify(m,r,q):
    adj,data=construct(m,r,q)
    assert min(map(len,adj))>=r*q
    assert len(adj)==data['core_n']+3*(m+r)*q
    count=check_symbolic_core(data)
    traces=check_no_C3_C5(adj)
    return dict(m=m,r=r,q=q,n=len(adj),minimum_degree=min(map(len,adj)),ratio=min(map(len,adj))/len(adj),limit=r/(3*(m+r)),same_type_3walks=count,odd_traces=traces)
'''
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent2_lower.py','w') as f:f.write(MODULE)
exec(MODULE)
for m,r,q in [(3,1,2),(4,1,2),(5,2,2),(6,2,2),(7,3,2),(8,3,1)]:
    print(verify(m,r,q),flush=True)

SHIFT = r'''
def shift_representation(N,k):
    assert k%2==1 and 1<k<=N
    vertices=list(itertools.combinations(range(N),k))
    ids={v:i for i,v in enumerate(vertices)}
    edges=[(ids[t[:-1]],ids[t[1:]]) for t in itertools.combinations(range(N),k+1)]
    labels=[set() for _ in vertices]
    for p,permutation in enumerate(itertools.permutations(range(N))):
        rank={v:i for i,v in enumerate(permutation)}
        for i,v in enumerate(vertices):
            minpos=min(range(k),key=lambda j:rank[v[j]])
            if minpos%2==1: labels[i].add(p)
    m=p+1; r=m*(k-1)//(2*k)
    assert all(len(label)==r for label in labels)
    assert all(labels[u].isdisjoint(labels[v]) for u,v in edges)
    return labels,edges,m,r

def extension_coloring(N,k,colors):
    """Verify the elementary chromatic reduction for any supplied proper coloring."""
    vs=list(itertools.combinations(range(N),k))
    assert set(colors)==set(vs)
    for t in itertools.combinations(range(N),k+1):
        assert colors[t[:-1]]!=colors[t[1:]]
    reduced={t:frozenset(colors[t+(x,)] for x in range(t[-1]+1,N))
             for t in itertools.combinations(range(N),k-1)}
    for t in itertools.combinations(range(N),k):
        assert reduced[t[:-1]]!=reduced[t[1:]]
    return reduced
'''
with open('workspace/agent2_lower.py','a') as f:f.write(SHIFT)
exec(SHIFT)
PROOF = r'''LOWER BOUND (fully elementary)

Fix c<1/9 and finite triangle-free H; write h=|V(H)|. Choose odd k>=3
large enough that alpha/(3(1+alpha))>c for alpha=(k-1)/(2k).
Let T_0=h, T_{i+1}=2^{T_i}. Choose N>max(k,T_{k-1}).
The shift graph F=S(N,k) has as vertices increasing k-tuples in [N], with
an edge between the two consecutive k-windows of each increasing (k+1)-tuple.
Then chi(F)>h: an l-coloring of S(N,j), j>=2, produces a coloring of
S(N,j-1) by at most 2^l colors, assigning each tuple the set of colors of
its right-extensions. For consecutive (j-1)-windows, the full j-tuple's
color belongs to the first extension set but not the second, because all
right-extensions of the second window are adjacent to that full j-tuple.
Iteration would imply chi(S(N,1))=N<=T_{k-1}.

Index m=N! coordinates by permutations pi of [N]. For a vertex v of F,
let L(v) be the coordinates where the pi-minimal element of v occurs at
an even position (positions numbered 1,...,k). Every label has size
r=m(k-1)/(2k)=alpha*m. Labels of adjacent vertices are disjoint: for their
combined (k+1)-tuple, a minimum at either endpoint leaves one window with
minimum at odd position 1 or k; an internal minimum switches parity between
the two windows.

Orient every F edge u->v arbitrarily and replace it by u-a_uv-b_uv-v.
Call the resulting graph D, and assign types 0 to original vertices, 1 to
a_uv and 2 to b_uv. Assign labels L(u), L(v), L(u), L(v) along each such
path. Equivalently a_uv gets L(v), b_uv gets L(u). Every same-type
3-edge walk in D has endpoints with disjoint labels. This follows directly
from subdivision vertices having degree 2: for type 0 it traverses one
subdivided F-edge, and for type 1 or 2 it traverses an end segment of one
subdivided edge, a branch vertex, then an end segment of another; the two
endpoint labels are labels of endpoints of one of these F-edges.

For each type i add m*q vertices W_i, q copies of each coordinate, and
r*q vertices P_i. Join W_i completely to P_i. Each D-vertex x of type i
is joined to copies of precisely the coordinates in its label. There are
n=s+3(m+r)q vertices, where s=|D|; all degrees are at least rq.
Choose integer q so rq>=c[s+3(m+r)q], possible by the chosen strict ratio.
For c=0 any positive q works.

There are no C3 or C5. D has girth at least 9. After deleting its edges,
the new graph consists of three bipartite components, one per type, all
D-vertices in the same side within each component. Thus every excursion
of a cycle through new vertices has even length and joins same-type
D-vertices. An odd cycle of length at most 5 not entirely in D can use
only one or three D-edges. One is impossible because D-edges change type.
Three forces a 3-path in D closed by a 2-path through a W_i vertex. Its
same-type endpoints would have intersecting labels, a contradiction.

Finally, a homomorphism to triangle-free H must send the original endpoints
of each subdivided F-edge to different vertices: otherwise its 3-path
would give a closed 3-walk in a simple triangle-free H. Its restriction to
V(F) would be a proper h-coloring of F, contradiction. This proves that
no c<1/9 has the required property, with no topological input.
'''
with open('workspace/agent2_lower_proof.txt','w') as f:f.write(PROOF)
for N,k in [(4,3),(5,3),(6,3),(6,5),(7,5)]:
    labels,edges,m,r=shift_representation(N,k)
    vertices=list(itertools.combinations(range(N),k))
    colors={v:i for i,v in enumerate(vertices)}
    for j in range(k,1,-1): colors=extension_coloring(N,j,colors)
    print('shift checks',N,k,'vertices',len(labels),'edges',len(edges),'m',m,'r',r,'alpha',r/m,flush=True)
    if N<=5:
        adj,data=construct_from_labels(labels,edges,m,r,1)
        assert min(map(len,adj))>=r
        assert len(adj)==data['core_n']+3*(m+r)
        print('FULL SHIFT RESERVOIR',N,k,'n',len(adj),'minimum degree',min(map(len,adj)),'core3',check_symbolic_core(data),'odd traces',check_no_C3_C5(adj),flush=True)
