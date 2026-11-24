# Whitney-periodic remodeling lemma (proposed complete proof)

## Data
A finite rooted 4-ary probability tree of depth L is given. Every child has conditional probability 1/4. At its terminal leaves are fixed invertible 2x2 matrices M, and vectors f,g. At every node s, let nu_s be its conditional terminal distribution. Suppose its matrix characteristic is at most A, i.e. the mixed p,q expression over two independent samples of nu_s is <=A. Write f_s=E_s f,g_s=E_s g.

Goal: construct a periodic matrix root M_real and compactly supported f_real,g_real on R, preserving the joint terminal distribution, such that [M_real]_{Ap}<=C_p A, and the Hilbert form approximates the lexicographic torus Hilbert form on the tree (for a prescribed ordering of four children on the circle).

## Whitney-period construction
On (0,1), use Whitney blocks (2^(-j-1),2^(-j)) for j>=1, together with their reflections about 1/2; the two central blocks meet at 1/2. Subdivide each block into N identical periods, and split each period into four equal child intervals. Put a rescaled recursively remodeled child profile in each child interval. Leaves are constant. At any node this preserves its conditional terminal law EXACTLY, since each period has four equal children and all periods together fill (0,1).

Adjacent child intervals at this generation have length ratios <=2, including transitions between Whitney blocks. There is no first interval at endpoints: lengths tend to zero there.

## Boundary averages
Let r=p or q and let T=M or M^{-*}, respectively. The finite terminal range gives constants B<infinity and m>0, uniform over all nodes, such that |T(x)v|^r<=B|v|^r and E_s|Tv|^r>=m|v|^r. For a boundary interval (0,t), every fully contained period has exactly the node-s mean moment. There is at most one incomplete period, of length <=C t/N. Thus

(1/t) int_0^t |T(x)v|^r dx <= E_s|Tv|^r + C B |v|^r/N <=2 E_s|Tv|^r

provided N>=CB/m. The same holds for intervals adjacent to 1. This bound is independent of all deeper remodeling parameters, because their full child distributions remain exact. Choose every N at least this common finite threshold.

## All real intervals
Take a nontrivial interval I inside the root cell. Descend through a child interval whenever all of I is contained in it. Finite tree depth ensures that either I reaches a constant leaf, or it meets at least two child intervals of a node s.

If I meets at least three child intervals, its smallest cover J by full child intervals satisfies |J|<=5|I|: each endpoint child has length at most twice its adjacent fully contained child. Every child moment is <=4 times its parent moment, by positivity and equal child probabilities. Consequently the moment average on I is <=20 E_s|Tv|^r.

If I meets exactly two children, both pieces are boundary-anchored in those children. The preceding boundary estimate bounds the average by <=8 E_s|Tv|^r. (If infinitely many children are met because I crosses an accumulation endpoint, apply boundary averaging at the corresponding parent/root boundary.)

Thus both the primal p-moment and dual q-moment norms for I are dominated, uniformly in directions, by fixed multiples of the corresponding conditional norms at ONE node s. Standard 2-dimensional reducing-matrix comparison then implies the interval mixed characteristic <=C_p A. The constants are independent of depth, B/m, and N.

Extend the root profile periodically. Intervals meeting multiple root periods are treated by the same cover/boundary argument (equal period lengths); intervals in one period were handled above. This proves the global all-interval characteristic bound.

## Hilbert local oscillation lemma
For bounded 1-periodic F,G with zero means, on a fixed interval J put F_N(x)=F(N(x-left(J))/|J|)1_J(x), and similarly G_N, with integer N. Then

lim_N int H_R F_N . G_N = |J| int_T H_T F . G.

Proof: first take trigonometric polynomials. The Fourier multiplier -i sign(xi) is asymptotically constant on the translate of the Fourier transform of 1_J centered at any nonzero frequency kN; Plancherel and disjoint frequency separation give the assertion termwise. Approximate arbitrary bounded periodic F,G in L2(T), use the uniform L2 boundedness of H_R, and scale. The same oscillations converge weakly to zero in L2(J).

For Whitney-periodic repetitions the lemma remains true: truncate to finitely many Whitney blocks, apply the preceding assertion on each, and note that cross-block terms vanish. For disjoint blocks, trim small neighborhoods of their endpoints; the cross-block Hilbert operator then has a bounded square-integrable kernel and is compact, so weak convergence kills the cross terms. The discarded tails are uniformly small in L2 because profiles are bounded and their total lengths tend to zero. Hence the limit is |J| times the periodic local form.

## Additive tree form
At each tree level refine all parent intervals by the Whitney-periodic child pattern. Its mean-zero difference from the old conditional-mean vectors converges weakly to zero as that level's frequency parameter tends to infinity. Therefore its cross terms with the previously fixed coarser functions vanish. Interactions between differences on distinct parent intervals vanish by the same trimmed-support compactness argument; interactions inside a parent interval converge to its periodic one-cycle Hilbert form times its length. The countable collection of parent intervals is handled by finite truncation plus bounded-profile L2 tails.

There are only finitely many levels. Choose their frequency parameters successively large, preserving earlier approximations. The final real Hilbert form is arbitrarily close to the sum over tree nodes of their probability times the prescribed one-cycle periodic Hilbert form. Joint distributions of M,f,g remain exact, so weighted primal/dual test norms are preserved.

Finally use f_real,g_real supported on the root period and the periodic bounded positive matrix weight W=(M_real^* M_real)^(p/2). Approximation by smooth compactly supported functions is legitimate because the finite terminal matrix range is uniformly elliptic; use H's ordinary unweighted Lp boundedness for convergence. The Hilbert lower bound follows by dual Holder.

## Remaining audit points
The preceding argument uses standard Plancherel and reducing-matrix equivalence. The combinatorial interval-cover assertion and the claimed finite-parameter sequential Hilbert limit should be independently audited. No external remodeling theorem has been assumed.
