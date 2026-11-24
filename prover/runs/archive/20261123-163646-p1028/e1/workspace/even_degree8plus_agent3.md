# All d>=8 exclusions for even n
Let G be dregular on n vertices. For each adjacent pair a,b, contract all other vertices into one vertex. Rayleigh monotonicity gives R_ab>=2/(d+1): the contracted network is a unit edge in parallel with two series bundles of d-1 unit edges. Foster's identity gives sum_{ab in E} R_ab=n-1.

Take a shortest u-v path P with l edges. Resistance distance is a metric, so
R_uv<=sum_{e in P}R_e
<=n-1-[dn/2-l]*2/(d+1)
=n/(d+1)+2l/(d+1)-1.
The vertices at path positions0,3,6,... have disjoint closed neighborhoods (otherwise a shortcut exists), each of size d+1. Thus floor(l/3)+1<=n/(d+1), and l<=3n/(d+1)-1. Consequently
 d R_uv <= A_d n - d-2d/(d+1), where A_d=d(d+7)/(d+1)^2.
The weaker bound dR<=A_d n-d suffices below.
A_d decreases for d>=2 because its derivative as a real function is (7-5d)/(d+1)^3.
For d>=9, A_d<=A_9=36/25<3/2, and -d<=-9<-33/4, so dR<(3/2)n-33/4, below both even-n targets.
For d=8, A_d=40/27; compare A_8 n-8 with (3/2)n-33/4: their difference is n/54-1/4>=0 for n>=14. Such graphs require n>=9, and in our domain n10,12 are covered by the dense-degree spectral bound already proved by agent1; for n>=14 this inequality applies directly. Thus d>=8 never improves the cubic construction for any even n>=10.
