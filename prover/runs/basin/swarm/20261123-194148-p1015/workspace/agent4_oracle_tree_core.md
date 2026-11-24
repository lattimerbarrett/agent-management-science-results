# Proposed complete Pi2 core: oracle-tree dumping

Put H=0' and J=H'=0''. Use a monotone H-computable approximation J_s to J. Columns are pairs (i,k). We construct an H-c.e. set D, with each column either finite initial segment or all omega. Let G be its full-column set. We ensure G is a proper Pi2^H set, 1-generic relative H, and S=skip(complement D) is e-equivalent to H-total join G.

## Oracle-tree implementation

Run a deletion-only finite-injury priority program with oracle J, described below. Its current G starts omega, and its state stores a finite set Z of deleted G bits, plus finite positive restraints and finite program statuses. It never undeletes bits, although it can cancel lower positive restraints. The program also reads an H-computable environment: the finite list of all D-dumps declared so far in the actual approximation construction. This list is NOT recomputed at a revisited node; all choices are memoized when that node is first created.

The actual construction is H-computable. Lazily build the tree of computation histories of this program as finite guesses at the J oracle vary. At stage s follow the program for s steps using J_s, creating missing history nodes and reusing existing nodes. Each oracle-use guess may be encoded as a finite initial segment sigma of J_s; branch whenever an additional oracle bit is needed. Other actions are deterministic from the stored state and are done once, at node birth, using the current actual finite dump history. A node carries all oracle answers used along its history. It is correct when these agree with J.

Before processing a new node at depth n, whose stored deleted set is Z, declare the dump
    B(n,Z)={(i,k): i notin Z and k<n}.
D is the union of all declared dumps. An infinite computable dump can of course be enumerated by dovetailing, so D is H-c.e. At any finite construction stage, the union B of all declared dumps is a computable set, uniformly from their finite list. All negative decisions below avoid this DECLARED union, not just the finite part already enumerated.

Correct nodes form one chain. Every finite correct node is eventually visited: induct on the finite number of steps/oracle uses; J_s eventually agrees with J below the finite use, and the running-time budget tends to infinity. Once a correct node is visited, it is never left by any later stage path. This uses monotonicity of J_s: true negative answers never change, and true positive answers are already enumerated. Thus all later newly created nodes are descendants of it. (Use step budgets increasing, and retain the whole memoized computation tree.)

Define G by deleting exactly those bits deleted along the correct chain. This complement is c.e. in J: J can simulate the H-construction and recognize correct finite oracle histories. If i belongs to G, all correct nodes retain i=1, so their unbounded-depth dumps fill D_i. If i does not belong to G, a finite correct node deletes i. After that node is first visited all future dumps omit i, so D_i is a finite initial segment. In particular G is precisely the full-column set.

## Priority program on the correct chain

Interleave three types of requirements in any computable omega-order.

(1) Genericity P_e: meet or avoid the e-th H-c.e. open subset U_e of Cantor space. At activation, choose a prefix eta of the current G which contains all current zeros and all higher protected positive bits. J decides whether eta has an extension tau in U_e. If so choose one, delete its zero bits, and protect all its one bits. If not, protect the one bits of eta. Declare done until a higher-priority action injures this requirement. Only deletions are made: eta includes all current zeros, so no chosen extension ever needs to undelete a bit.

(2) Properness Q_e: ensure G differs from the e-th J-computable characteristic function. Choose a fresh x and protect its current value 1. Simulate Phi_e^J(x) one step at a time, without blocking other strategies. If it outputs 1, delete x. If it outputs any other value leave x=1. Declare done if it halts, otherwise retain the positive restraint. Higher injury resets to a fresh x. After higher stabilization, a total characteristic computation disagrees with G at x.

(3) Skip control N_e for the c.e. hypergraph F_e of finite supports of the diagonal e-th enumeration computation. Let P be the finite set of all higher protected positive G bits. Let B be the union of all dumps declared up to and including this node. H decides
    every F in F_e meets B union (P x omega).
This is an ordinary Pi1 question because B and P x omega are computable. If yes, declare done until higher injury. If no, find a finite edge F avoiding that union. Delete from G every column index appearing in F. These indices are outside P, so higher positive restraints are respected. Declare done. The actual D avoids F forever if this action occurs at a correct node: F avoids all past declared dumps, and every future node descends this action and omits all its columns. The deletion is permanent even if the strategy is later injured.

When a strategy changes a finite restraint or deletes G bits, initialize lower strategy statuses/positive restraints, but NEVER remove any G zeros. Each strategy acts finitely after higher stabilization: P_e acts once, Q_e acts at most twice (reserve and possibly delete), N_e acts once. Hence usual induction gives finite injury, the genericity and properness requirements are met, and every N_e eventually acts with stable higher positive set P contained in the final G. Oracle computations deciding P_e are finite; waiting Q_e computations are dovetailed and do not prevent the program from having infinitely many steps.

## Computing S from H join G

Enumerate, with oracle H, every pair (e,P) for which there exists a finite initial dump union B satisfying
    every F in F_e meets B union (P x omega).
The quantification over actual dump unions is H-effective, and the displayed coverage test is H-decidable. Use the finite positive G premise P to enumerate e. Every such rule is sound: B subset D and P subset G implies P x omega subset D. Thus the resulting operator is below S.

Conversely suppose e belongs to S, i.e. F_e is hit by D. Consider the eventual N_e action after higher stabilization on the correct chain. Its negative case would permanently make an edge disjoint from D, impossible. Therefore it took the positive case. The protected set P is included in final G, and the actual finite dump union B at that action witnesses one of the enumerated upper rules. Thus S<=_e H-total join G.

The reverse holds because all skips bound H-total, and G<=_m S: let e_i index the diagonal operator with supports all singleton sets {(i,k)}, k in omega. Then e_i belongs to S exactly when the entire column D_i is full, exactly when i belongs to G.

## Consequence

A=complement D is Pi1^H=Pi2 ordinary. Every Pi2 enumeration degree is weakly cototal. We have S_A equivalent to X=H-total join G.

G is Pi1^J=Pi2^H by the correct-node enumeration, but not J-computable by Q_e. Thus G is not Sigma2^H. By P_e it is 1-generic relative H. The established generic skip formula gives
    skip(X) equivalent to complement G join H',
which is equivalent to H'=J since complement G is Sigma2^H. If X were cototal, the cototality test would imply X<=_e skip(X)<=_e J; then G would be Sigma2^H, contradiction. Hence S_A has noncototal degree.

THIS DOCUMENT NEEDS TEAM AUDIT, especially correctness and persistence of nodes in the adaptive memoized oracle computation tree. It is a proposed core proof, not yet asserted established.
