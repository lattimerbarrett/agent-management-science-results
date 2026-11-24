# Sign patterns for two parallel hyperplanes x=a and x=b.
for a,b in [(0,1),(0,0),(1,0)]:
    roots=sorted(set([a,b]))
    samples=[roots[0]-1]+[(x+y)/2 for x,y in zip(roots,roots[1:])]+[roots[-1]+1]
    patterns=[(1 if x>a else -1,1 if x>b else -1) for x in samples]
    print((a,b), patterns, 'missing:', set([(1,1),(1,-1),(-1,1),(-1,-1)])-set(patterns))
print('For nonparallel normals the affine map to R^2 is surjective; all four inverse images of open quadrants are nonempty and convex.')