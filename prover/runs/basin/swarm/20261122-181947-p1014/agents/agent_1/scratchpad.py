from sage.all import libgap
g=libgap.SmallGroup(1944,2295);f=g.FrattiniSubgroup();P=g.SylowSubgroup(3);Q=g.FactorGroup(f).SylowSubgroup(3)
print(P.StructureDescription(),Q.StructureDescription(),P.IsCyclic(),Q.IsCyclic())
print(g.StructureDescription(),g.FactorGroup(f).StructureDescription())
