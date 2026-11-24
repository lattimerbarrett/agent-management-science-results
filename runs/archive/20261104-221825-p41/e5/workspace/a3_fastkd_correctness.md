# Exact facet-mask k-decomposability checker

`a3_fastkd.kd(fs,k)` assumes `fs` is a tuple of distinct facets all having the same cardinality. Each facet is a nonnegative integer bitmask. All calls in our computations satisfy this assumption, including recursive calls.

For a nonempty candidate face sigma and a facet F containing sigma, the maximal faces of 2^F which avoid sigma are precisely F-{v}, v in sigma. Consequently deletion is pure of the original dimension if and only if each such ridge lies in some other original facet. Since all original facets have the same size, any other facet containing F-{v} automatically avoids sigma (otherwise it equals F). Thus purity is equivalent to the code's test that every indicated ridge has facet-degree at least two.

When this holds, deletion facets are exactly original facets not containing sigma, and link facets are exactly F-sigma over original facets containing sigma. There are no containments among either collection, because all members in each collection have equal cardinality. The checker recurses on precisely these facet tuples, after testing every nonempty face sigma of size at most k+1. Its enumeration over vertex subsets also includes nonfaces, which are immediately discarded. A one-facet complex is exactly a simplex, including bitmask zero for the simplex {emptyset}.

The recursion terminates: deletion strictly reduces the number of facets, while link strictly reduces facet cardinality; both quantities never increase. Cache eviction affects runtime only, not truth values. Thus a False result is an exhaustive non-decomposability certificate in the sense that all possible shedding faces have been excluded recursively, and True asserts the exact recursive definition.

A useful reproducible distinction is `python workspace/a3_verify_bad_add.py`: an edge-decomposable pure three-complex on eight vertices becomes non-edge-decomposable after a shelling-legal tetrahedron addition. This is NOT a zero-extra completion obstruction, since other legal additions are available.
