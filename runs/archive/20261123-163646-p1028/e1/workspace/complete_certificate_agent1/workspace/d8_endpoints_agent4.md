# Degree-eight endpoint atoms: all orders, analytic proof
Use the valid two-level2/4-cut decomposition from odd_degree6_agent4.md, but every original vertex now has degree8. Point-terminal atoms have h2 or4 boundary incidences, hence size a>=9 by simplicity. Uniform boundary currents are1/2 or1/4. The internal transshipment has capacities1/6 by the degree-independent even-cut argument already proved. The required endpoint defect, after assigned outside energy and singleton charges, is gamma=139/360.

## General DAG estimate
Scale by12. Integer internal flows have edge capacity2 and total positive injection<=12. Cancel cycles and topologically order a vertices. Write W=sum_e j_e and L=sum_e j_e times indexdistance. Then L<=12(a-1). At a vertex with total incoming q and outgoing r, capacity2 and simplicity force weighted incident length at least q^2/4+q/2+r^2/4+r/2: fill the nearest predecessor/successor slots, two units per edge, to minimize length. Summing and Cauchy gives 2L >= W^2/(2a)+W. Substituting W=6a-3 exceeds24(a-1) by3+9/(2a)>0, so integer W<=6a-4. Energy <=2W/144<=a/12-1/18.
For a>=14, outside energy plus any singleton charge is at most1/4 (h2 tail has outside1/4 and no singleton charge; h4 tail has outside1/8 and at most one singleton charge1/8). Thus defect against a/8 is >=a/24-7/36>=7/18>139/360.

## Dense tails of orders9..13
Let p_v be the port-incidence deficits, sum p=h. The internal graph is K_a minus a graph with degrees a-9+p_v. For any graph Q, lambda_max(L_Q)<=max_{xy edge}(deg_Q(x)+deg_Q(y)): use the oriented incidence matrix and its edge-by-edge Gram matrix row absolute sums. Therefore lambda_2(internal)>=18-a-h. For an injection vector j of zero sum, energy j^T L^+ j <= ||j||^2/lambda_2.

For h2 the prescribed injection is p/2-unit_at_target, with squared norm<=2. Consequently E<=2/(16-a). For a9,10,11,12,13, the exact rational inequalities a/8-1/4-2/(16-a)>=139/360 hold (checker attached). This covers distinct/coincident ports, whether or not at the target.

For h4, a non-target vertex cannot have p_v4: it would induce a further nested size-four cut, contrary to maximality. Thus the squared injection norm of p/4-unit_at_target is <=13/8. The gap18-a-h=14-a gives E<=13/[8(14-a)]. For a9..12 these exact inequalities a/8-1/4-E>=139/360 hold.

It remains h4,a13. If at least one port incidence meets the target, reverse the flow: its total positive injection is at most9 in scale12. The elementary DAG estimate sum j^2<=C(F+C)(a-1)/2 gives energy<=11(a-1)/144=11/12, sufficient. If no port meets the target, reverse the flow to have a UNIQUE source, the target, of net supply12. In an acyclic flow its incoming flow is zero and outgoing flow12. Hence sum_out q^2>=144+(W-12)^2/12 and sum_in q^2>=W^2/12. The weighted-length lower bound sharpens to
2L >=36+[(W-12)^2+W^2]/48+W.
If W>=72, the RHS is at least291, contradicting2L<=288. Thus W<=71 and E<=2W/144=71/72. Finally13/8-1/4-71/72>=139/360. This includes the worst outside-plus-singleton charge1/4.

Every endpoint atom therefore retains margin >=139/360 after its assigned outside energy and possible singleton charge. The proof is fully analytic; workspace/check_d8_endpoints_agent4.py checks every finite rational inequality and both symbolic DAG substitutions.
