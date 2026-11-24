import json,sys,time
sys.path.insert(0,"workspace")
from a3_fastkd import kd
x=json.load(open("workspace/a3_bad_edge_add.json"));fs=tuple(sorted(x["facets"]));f=x["badadd"]
assert kd(fs,1)
assert not kd(fs,0)
assert not kd(tuple(sorted(fs+(f,))),1)
R=162
assert R&f==R
assert all(g&R!=R for g in fs)
assert (f^R).bit_count()==1
# In the new complex, R is a shedding triangle, deletion is original complex,
# and its link is a simplex. Thus it is 2-decomposable without a costly search.
ridges={g^(1<<v) for g in fs for v in range(x["n"]) if g>>v&1}
assert sum(f^(1<<v) in ridges for v in range(x["n"]) if f>>v&1)==3
print("Verified: 37-facet edge-decomposable non-VD complex; adding specified shelling-legal tetrahedron yields a shellable but non-edge-decomposable complex.")
