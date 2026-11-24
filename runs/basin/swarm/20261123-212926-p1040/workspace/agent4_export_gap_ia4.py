from sage.all import libgap as gap
from pathlib import Path
import json,time
print(gap.eval('LoadPackage("lpres" : OnlyNeeded := true);'),flush=True)
t=time.time();F=gap.FreeGroup(4);A=gap.AutomorphismGroup(F);e=gap.EmbeddingOfIASubgroup(A);G=gap.Source(e)
print('Gready',time.time()-t,flush=True)
fg=list(gap.FreeGeneratorsOfLpGroup(G))
R=list(gap.IteratedRelatorsOfLpGroup(G));S=list(gap.EndomorphismsOfLpGroup(G))
print('sizes',len(fg),len(R),len(S),time.time()-t,flush=True)
D={'names':[str(x) for x in fg],'rels':[gap.LetterRepAssocWord(w).sage() for w in R],'endomorphisms':[[gap.LetterRepAssocWord(gap.Image(s,x)).sage() for x in fg] for s in S],'convention':'GAP left-to-right map composition, comm=x^-1 y^-1 x y'}
Path('workspace/agent4_gap_ia4_data.json').write_text(json.dumps(D,default=int))
print('exported',time.time()-t,flush=True)
