# Constructive bound b(d,k) <= d-2 for every d>=3,k>=1

Use the cone-saturation lemma (`agent2_cone_lemma.md`) and full-boundary-addition lemma (`agent2_fullboundary_lemma.md`).

## Preliminary facts
A pure k-decomposable complex admits an ordering of its facets whose every nonempty initial segment is k-decomposable: recursively order deletion facets, then facets sigma joined to recursively ordered link facets. During the latter part sigma remains shedding. The same reasoning shows k-decomposability implies shellability.

Its pure codimension-one skeleton is k-decomposable. For a shedding face sigma which remains a face of the skeleton, use sigma again, with deletion the corresponding skeleton of the old deletion and link the corresponding skeleton of the old link. If sigma was a facet, purity of its deletion forces every proper face of sigma into a remaining facet. Thus the codimension-one skeleton is exactly that of the deletion, and facet-count induction applies. Base cases are simplices, whose pure skeleta are vertex-decomposable (delete a vertex until the simplex case).

It follows that Delta can be extended to its near-cone Delta union a*skel_{d-1}(Delta), using one new vertex a and facets aH for all ridges H of Delta: take the above facet-prefix order of the ridge skeleton. At every nonempty stage a is shedding, deletion is Delta (every H was already a face), and link is the corresponding k-decomposable prefix.

## Dimension two base, no extra vertices
A pure k-decomposable 2-complex has connected graph, directly by recursion: a shedding face of size at least two has deletion spanning all vertices, whose graph is connected inductively; for a shedding vertex v, the deletion graph spans all other vertices and v has a neighbor there. If the graph is not complete, choose an induced length-two path x-y-z. The missing triangle xyz has exactly two present edges. Add it: its restriction face is the missing edge xz, of size2<=k+1; it is a shedding face with old complex as deletion and simplex link. If the graph is complete but a triangle is missing, its full boundary is present, so the full-boundary lemma permits its addition. More generally any missing triangle with at least two present edges may be chosen. Each step preserves k-decomposability. A noncomplete connected graph always has such an induced path, and the process is finite. Thus all missing triangles can be filled with zero extra vertices.

## Induction
For d>=3 let A consist of d-2 new vertices, choose a in A, and put B=A minus a. First build the near-cone on a as above. Let Gamma_0=skel_{d-1}(Delta). By the dimension induction hypothesis Gamma_0 has a k-decomposability-preserving completion Gamma_i on V union B, using |B|=d-3 vertices (the dimension2 base handles d=3). For each newly added facet H of Gamma_i, add aH upstairs. At each resulting stage
 E_i = Delta union a*Gamma_i.
All ridges of the old d-facets of Delta lie in Gamma_i, so E_i is k-decomposable by the cone-saturation lemma. This bypasses the invalid claim that a remains shedding: unsupported H may occur in its deletion, but other shedding faces supplied by the cone lemma apply.

When Gamma_i is full, every d-facet containing a is present. Now add all missing d-facets not containing a in arbitrary order. At each stage the link base Gamma is the full (d-1)-skeleton on V union B, which is vertex-decomposable, and the top facets avoiding a are arbitrary. The cone-saturation lemma shows every such stage is vertex-decomposable. Thus the final complex is the full d-skeleton on V union A, and every intermediate is k-decomposable.

This proves only b(d,k)<=d-2. The sharper cap k-1 for k<d-1 and the lower bounds are not established here.
