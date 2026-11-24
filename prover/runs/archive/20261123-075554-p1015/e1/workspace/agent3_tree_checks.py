from itertools import product
from pathlib import Path

# -1 is the infinity outcome. Nonnegative symbols are candidate outcomes.
def prefix(a,b):
    return b[:len(a)] == a

def bank(sigma, point):
    return sigma == point[0]

def region(sigma, point):
    return prefix(sigma, point[0])

def body(sigma, point):
    node = point[0]
    return bank(sigma, point) or (prefix(sigma,node) and len(node)>len(sigma)
                                  and node[len(sigma)] >= 0)

def Z(sigma, point):
    return any(symbol == -1 and body(sigma[:i],point)
               for i,symbol in enumerate(sigma))

def run_checks():
    alphabet = (-1,0,1)
    nodes = [s for n in range(5) for s in product(alphabet, repeat=n)]
    points = [(s,k) for s in nodes for k in range(2)]
    counts = {'finite_child_protection':0,'infinite_ancestor_protection':0,
              'refutation_safety':0,'infinity_branch_partition':0}
    for sigma in nodes:
        if len(sigma)>3:
            continue
        for j in (0,1):
            child = sigma+(j,)
            for point in points:
                protected_allowed = not(Z(sigma,point) or bank(sigma,point)
                                        or region(child,point))
                if region(child,point):
                    assert not protected_allowed
                    counts['finite_child_protection'] += 1
                # Refutation deletes R_j subset of B_sigma and child subtree.
                deleted = (bank(sigma,point) and point[1] == j) or region(child,point)
                if deleted:
                    assert not protected_allowed
                    counts['refutation_safety'] += 1
        for i,symbol in enumerate(sigma):
            if symbol != -1:
                continue
            ancestor = sigma[:i]
            for point in points:
                if body(ancestor,point):
                    assert Z(sigma,point)
                    counts['infinite_ancestor_protection'] += 1
        for point in points:
            # Entire node-region partitions into B, finite-child regions,
            # and infinity-child region; hence Z-body and infinity region
            # are disjoint and exhaustive within node region.
            assert not(body(sigma,point) and region(sigma+(-1,),point))
            assert region(sigma,point) == (body(sigma,point) or region(sigma+(-1,),point))
            counts['infinity_branch_partition'] += 1
    return counts

if __name__ == '__main__':
    print(run_checks())
    Path('workspace/agent3_tree_checks.py').write_text(Path(__file__).read_text())
    Path('workspace/agent3_lower_outline.md').write_text('''# Lower construction outline (ordinary-c.e. bank issue repaired)

Use a coding domain of triples (n,b,k), and a free domain of labels (sigma,k), sigma a finite string over {infinity,0,1,...}. Coding removals only have b=0prime(n), and eventually at least one such removal for each n. Free-domain region T_sigma consists of labels at nodes extending sigma; B_sigma is the labels at sigma itself. Partition B_sigma into uniformly computable infinite banks R_sigma,j, j coding finite G_j. Every region and the union of all finite-child regions is computable.

For each sigma let e=length(sigma), and computably obtain x_sigma for the enumeration operator which outputs ALL numbers exactly when its input meets B_sigma. Thus x_sigma belongs to skip(A) iff B_sigma is a subset of D=complement(A). No recursion theorem or oracle-dependent axiom enumeration is needed.

Put L_sigma = B_sigma union all T_(sigma concatenated j), j finite; equivalently T_sigma minus T_(sigma concatenated infinity). Put Z_sigma equal to the union of L_tau over those ancestors tau of sigma where sigma takes outcome infinity. These are computable sets, uniformly in the finite node sigma.

Node sigma monitors candidates j such that (x_sigma,G_j) enters W_e. It has at most one active candidate, selects each unrejected candidate eventually, and permanently records rejections. Candidate j has obligations (y,H) in W_y, y in G_j. At a visit, process at most one new obligation observed by the present ordinary enumeration stage; even if no new obligation exists, continue to visit its finite child j. This ensures no blocking on a finite obligation list.

At a finite construction stage, planned D is a finite union of whole computable regions/banks plus finitely many individual points. Whole-set enumerations may be represented immediately in planned D and dovetailed into the actual c.e.-in-0prime enumeration. Thus A_stage=complement(planned D) is computable uniformly in the finite stage parameters. For an active obligation put Q=A_stage minus (Z_sigma union B_sigma union T_(sigma concatenated j)). With 0prime decide whether some z in H belongs to K_Q={z:z in Gamma_z(Q)}. If yes, find an ordinary finite Q-witness F for such z and protect F. If no, release all protections belonging to this candidate and its finite-child subtree, enumerate R_sigma,j and T_(sigma concatenated j) into D, reject j, and take outcome infinity.

At a reset/idle infinity visit, additionally enumerate a growing finite initial segment of L_sigma into D, then visit the infinity child. These background deletions happen ONLY at infinity visits. In particular, if some candidate j survives forever, background deletion at sigma stops and all off-path regions freeze. A never-activated R_sigma,j has suffered only finitely many background point deletions at its finite activation stage, so it retains an infinite tail unless the node is already on a dead branch.

A global stage recursively visits at most stage-many levels. Each coding requirement n gets a stage at which it chooses one fresh 0prime-correct coding marker outside all presently protected finite sets. Future witnesses avoid planned D, hence preserve that marker. Coding meets every n and gives T(0prime) <=e D; all D is c.e. in 0prime, hence D <=e T(0prime). Therefore A is Pi2 and weakly cototal.

Live protections should NOT be discarded merely because their nodes are temporarily unvisited. In particular infinity-child protections persist through the parent's finite candidate episodes: they avoid L_parent, so all parent deletions are harmless. Release protections only when their supporting candidate is rejected or their entire finite-child subtree is deleted. The global protection audit is supplied by agent2.

True path: at each infinitely visited node either one candidate eventually remains active (finite outcome j), or no candidate survives (infinity outcome). In the latter case infinitely many infinity visits imply L_sigma subset D at the limit, including never-activated finite child pools. In the former case R_sigma,j retains an infinite tail and all obligations are eventually met with protected witnesses. True-path regions are not entirely deleted by ancestor actions. Every true-path node is visited infinitely often by induction.

For a true-path sigma, Z_sigma subset D, because each contributing ancestor takes true outcome infinity. If j survives, its protected witnesses show every W_y axiom H, y in G_j, meets K_A, so G_j subset skip(skip A). The retained R_sigma,j tail makes x_sigma not in skip A. Hence Gamma_e(skip(skip A)) contains x_sigma while skip A does not.

If every candidate j is rejected, B_sigma subset D and x_sigma belongs to skip A. Each rejection has an obligation (y,H) with H subset skip(Q) at that stage. In the final construction, A subset Q: Z_sigma subset D by true-path ancestry, B_sigma subset D by infinitely many resets, T_sigma,j subset D by its rejection, and actual A is below A_stage. Hence H subset skip A, so y is not in skip(skip A), refuting G_j as an output witness. All candidate G_j are therefore invalid, so Gamma_e(skip(skip A)) omits x_sigma. Again inequality.

Finally degree(X) is cototal iff X <=e skip(X). Apply to X=skip(A): all operators e have been diagonalized, so skip(A) is not cototal.
''')
