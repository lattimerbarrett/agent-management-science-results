# Odd-n lower bound
Use unit resistors and the commute identity C_uv=4n R_uv in a 4regular graph.
A cap C_b has b vertices, one distinguished vertex p of degree2, all others degree4.
A bulk B_b has b vertices, distinguished p,q of degree2, all others degree4.
The explicitly listed edge sets are in odd_construction.py. Exact grounded Laplacian inversions in check_modules() give:
C6: R-ecc(p)=4/5; C7:104/115; C9:52/45; C10:31/20;
B6: R(p,q)=5/4; B8:3/2.
In every case this also equals the full resistance diameter (the code checks this exactly).

Take two caps, and place a sequence of bulks between them. Identify cap/bulk ports consecutively, using each bulk's two ports once; the right cap's port is identified with the final bulk port. If there are no bulks, identify the caps' ports. The result is connected, simple and4regular: each identified pair contributes degree2+2=4, with no other identification. Its order is a+b-1+sum(bulk_order-1). Choose farthest vertices from the ports in the two caps. By the series law at articulation vertices their resistance is the sum of cap eccentricities and bulk port resistances.

For n mod5 use the following caps and optional exceptional bulk, then add k copies of B6, where k is the unique nonnegative integer making the order n:
 residue0: C6,C10; base order15, base resistance47/20.
 residue1: C6,C6; base order11, base resistance8/5.
 residue2: C6,C7; base order12, base resistance196/115.
 residue3: C6,C6 with B8; base order18, base resistance31/10.
 residue4: C6,C9; base order14, base resistance88/45.
For odd n>=15, the smallest orders in the five classes are15,21,17,23,19 respectively; thus k>=0 in every permitted case.
Every B6 increases order by5 and resistance by5/4. Therefore n/4-R is constant within each residue, with values
7/5,23/20,149/115,7/5,139/90.
Multiplying R by4n gives exactly the five claimed odd-n lower bounds.

Furthermore the chosen pair realizes the constructed graph's resistance diameter: each module has diameter equal to its distinguished distance/eccentricity, so any pair in different modules has distance at most the sum between the two extreme cap vertices; any pair in one module is bounded by that module's diameter, also at most that sum. Series additivity at identified ports proves the assertion. Full exact resistance matrices verify this independently for every odd n15..65 when odd_construction.py is run.
