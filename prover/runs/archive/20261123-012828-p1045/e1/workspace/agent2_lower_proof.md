# Complete lower bound
Fix alpha in (0,1] and epsilon in (0,1), and write C for the stated piecewise expression and N=floor((C-epsilon)n).

## Constant branch
For C=2 split N vertices as evenly as possible into two classes, color all cross edges red and internal edges blue. Red is triangle-free. The blue books have at most ceil(N/2)-2 pages, less than n for sufficiently large n.

## Three-part random branch
Put p=sqrt(3 alpha/C), q=1-p. The identity
C(1+2q^2)/3=1
follows from C=1+2alpha/3+(4/3)sqrt(alpha(3-2alpha)). Partition N vertices into three classes whose sizes differ by at most one. Color all internal edges blue and independently color each cross edge red with probability p.

Conditional on any potential spine being red (which is possible only for cross edges), its number of red common neighbors has mean at most p^2(N/3+1)=alpha N/C+p^2.
For a blue internal spine in class i, its blue common-neighbor count has mean (|V_i|-2)+q^2(N-|V_i|), at most N(1+2q^2)/3+1.
For a blue cross spine in classes i,j with remaining class k, its mean is q(|V_i|+|V_j|-2)+q^2|V_k|, at most N(2q+q^2)/3+2. Because 1+2q^2-(2q+q^2)=p^2>=0, this is at most N/C+2.

## Homogeneous branch
Put p=sqrt(alpha)/(1+sqrt(alpha)), and independently color every edge red with probability p. With C=(1+sqrt(alpha))^2, the red and blue conditional common-neighbor means are at most alpha N/C and N/C respectively.

## Concentration (both random models)
For a fixed potential edge, conditional on its color, its codegree is a sum of independent Bernoulli random variables and deterministic summands; conditioning does not change any of the incident edges used in the count. In every case the conditional red mean is at most alpha N/C+3 and blue mean is at most N/C+3. Let t=alpha epsilon n/(2C). For all sufficiently large n both mean+t values are strictly below alpha n and n respectively. Hoeffding's inequality gives upper-tail probability at most exp(-2t^2/N) for each edge and color. A union bound over the fewer than 2N^2 events gives failure probability at most 2N^2 exp(-2t^2/N)=o(1). Thus a suitable coloring exists. Having fewer than alpha n red common neighbors in particular means fewer than ceil(alpha n) pages.

## Transitions
Parameterize the three-part construction by p, with alpha=p^2/[1+2(1-p)^2] and C=3/[1+2(1-p)^2]. Its derivative alpha'(p)=2p(3-2p)/[1+2(1-p)^2]^2 is positive for p in [0,1]. At p=1/2, alpha=1/6 and C=2. Equality with C=(1+sqrt(alpha))^2 is equivalent to p+sqrt(1+2(1-p)^2)=sqrt(3), giving p=4-2sqrt(3), alpha=(52-16sqrt(3))/121. All squaring steps have positive sides on p in [1/2,4-2sqrt(3)]. Therefore either model is valid at the latter endpoint; the bipartite and three-part models both apply at alpha=1/6.

The program lower_bound_checks.py verifies the exact algebra using SymPy and computes full codegree tables for seven seeded finite colorings using NumPy. It has been run successfully.
