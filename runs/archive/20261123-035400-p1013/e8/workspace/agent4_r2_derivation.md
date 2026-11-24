# Odd bipartite finite-gadget cycle comparison (complete proof)
Let a=m+1,b=m, and let C_0=c(K_{a,b}). For j>=0 define
I_j= sum_{l>=0}1/[l!(l+j)!] (these equal I_j(2), but no Bessel facts are needed).
Writing H_0=(m+1)!(m-1)!/2, direct cycle enumeration gives
 C_0/H_0=sum_{j=0}^{m-2} [m/(m-j)]/[j!(j+1)!] = I_1+O(1/m).
For a FIXED internal edge in the larger class, the number of cycles using it is
 A_m=m!(m-1)! sum_{j=0}^{m-1}1/(j!^2),
so A_m/H_0=2 I_0/(m+1)+o(m^-2).
For a FIXED internal edge in the smaller class,
 B_m=(m-2)!(m+1)! sum_{j=0}^{m-2}1/[j!(j+2)!],
so B_m/H_0=2 I_2/(m-1)+o(m^-2).

For any FIXED bounded internal gadgets F_A,F_B with e_A,e_B edges, all cycles using at least two internal edges contribute O(C_0/m^2): select the internal linear forest (there are only finitely many choices), contract its e>=2 edges, then enumerate alternating cycles through the mandatory supervertices. The resulting ratio is O(m^-e); isolated entirely-internal cycles are negligible. Thus
 c(K_{m+1,m}+F_A+F_B)/C_0
 =1+[2/(m I_1)](e_A I_0+e_B I_2)+O(m^-2).
The O constants depend only on the fixed gadgets.

Proposed edge-extremal profiles have e_A=e_B=3; competitor has e_A=4,e_B=0. Its first-order advantage is
 [2/(m I_1)](I_0-3 I_2).
A coefficientwise telescoping calculation gives I_0-I_2=I_1:
1/(l!^2)-1/[(l-1)!(l+1)!]=1/[l!(l+1)!] after matching indices.
Hence I_0-3 I_2=3 I_1-2 I_0>0. The last strict inequality follows from rational series bounds; agent4_bipartite_checks.py certifies 2/3<I_1/I_0<3/4 using20 terms and geometric tail bounds.
Therefore for all sufficiently large odd n=2m+1, the competitor has more cycles than EVERY 3+3 edge-extremal profile, regardless of shapes of its3-edge gadgets.

Exact both-part cycle enumeration (agent4_r2_counter.py) checks the comparison for all4 combinations star3/triangle on each side; m=150,200,500,1000 all favor the competitor. The exact counter was independently checked against brute DFS enumeration for386 enriched bipartite graphs on at most9 vertices.

This proves the cycle-comparison part. The separate forbidden-profile realizer and global extremal structural argument are required to infer ex=t2+6.
