# H14 cycle separation at coefficient 1/4

Let m be even and let B_m be K_{m,m} with a perfect matching in its first part. Write h_m=m!(m-1)!/2 and
F=I_0(2sqrt2), beta=sqrt2 I_1(2sqrt2)/F>0.

Then c(B_m)~h_m F. For any fixed bounded collection of edge changes in the two parts (all endpoints fixed in number),

 c(modified B_m)/c(B_m)=1+(beta/m)(Delta e_A+2 Delta e_B)+O(m^-2).

The big-O constant can depend on the fixed modification. To see the coefficients, specify one fixed A edge and then j other matching edges, omitting s unused A vertices. Contraction into alternating cycles gives the normalized leading coefficient

 (2/m) sum_{s,j>=0} 1/[j!s!(s+j+1)!]
 = (2/m) sum_{k>=0} 2^k/[k!(k+1)!]
 = (sqrt2/m) I_1(2sqrt2).

For a fixed B edge, choose j A-matching edges and omit t A vertices. Balance forces j+t-1 omitted B vertices; the coefficient is (2/m) sum_{j,t>=0,j+t>=1}1/[j!t!(j+t-1)!]=(4/m) sum_{k>=0}2^k/[k!(k+1)!]=(2sqrt2/m)I_1(2sqrt2), twice the A coefficient. Equivalently use the two-part matching limit I_0(2sqrt((1+2rho_A)(1+2rho_B))) and differentiate in rho_B at (rho_A,rho_B)=(1/2,0); the same contraction sum gives the derivative directly. Two prescribed new edges contribute O(m^-2), even if adjacent: a connected path of two edges contracts two vertices, while there are only O(1) choices. Deleting or introducing finitely many old matching edges only changes these coefficients by O(m^-2). The factorial denominators permit termwise expansion; tails can be bounded uniformly by their exponential/Bessel factorial majorants. Hence the displayed expansion holds for arbitrary fixed changes, not just a single edge.

The edge-extremal graph identified by agent3 is obtained from B_m by replacing three matching edges (on six vertices) by two triangles. Thus its A-edge net change is +3 and B-edge change zero:

 c(G_edge)/c(B_m)=1+3 beta/m+O(m^-2).

The alternative graph retains the perfect A matching and adds two disjoint B edges:

 c(G_alt)/c(B_m)=1+4 beta/m+O(m^-2).

Therefore c(G_alt)>c(G_edge) for all sufficiently large even m, while G_alt has one fewer edge. No numerical Bessel inequality is needed: beta>0 follows immediately from its positive series.

Exact finite counting formulas and brute-force validations are implemented in agent2_h14_cycles.py. The component-polynomial formula includes the two internal triangle cycles themselves, though they are asymptotically negligible.
