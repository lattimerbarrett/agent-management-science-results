  
############################################################################
##
#M IA group
##
############################################################################
InstallMethod( EmbeddingOfIASubgroup, "for a free group automorphism group",
        [ IsAutomorphismGroupOfFreeGroup ],
        function(A)
# conventions on generators:
# M[i][j][k] is M_{x_i,[x_j,x_k]} if all variables i,j,k are <= n. x_i^-1 is represented as i+n.
# M[i][j][k] is a variable only if j<k. If j>k, it is stored as M[i][k][j]^-1.
# C[i][j] is C_{x_i,x_j} if i,j <= n. If j>n, then it is C_{x_i,x_{j-n}}^-1.
#
# Beware that GAP composes maps left-to-right, while the article composes maps right-to-left.
# GAP's commutator is [g,h] = g^-1h^-1gh, while the article's commutator is ghg^-1h^-1.
# Therefore, in converting an article formula to a GAP formula, multiplication order must be reversed,
# and commutators must be switched from [g,h] to [h,g].
#
    local n, F, G, C, M, i, p, q, r, s, t, u, v, rels, endos, Gendos, epi, alpha;
    
    G := Source(One(A)); # the free group
    n := RankOfFreeGroup(G);
    
    C := List(Arrangements([1..n],2),p->Concatenation("C(",String(p[1]),",",String(p[2]),")"));
    M := [];
    for p in Arrangements([1..n],3) do
        if p[2]>p[3] then continue; fi;
        Add(M,Concatenation("M(",String(p[1]),",[",String(p[2]),",",String(p[3]),"])"));
    od;
    F := FreeGroup(Concatenation(C,M));
    i := 1;
    epi := [];
    C := List([1..n],i->[]);
    for p in Arrangements([1..n],2) do
        C[p[1]][p[2]] := F.(i);
        C[p[1]][p[2]+n] := F.(i)^-1;
        q := ShallowCopy(GeneratorsOfGroup(G));
        q[p[1]] := q[p[2]]*q[p[1]]/q[p[2]];
        Add(epi,GroupHomomorphismByImages(G,q));
        i := i+1;
    od;
    M := List([1..2*n],i->List([1..2*n],j->[]));
    for p in Arrangements([1..n],3) do
        if p[2]>p[3] then continue; fi;
        M[p[1]][p[2]][p[3]] := F.(i);
        M[p[1]][p[3]][p[2]] := F.(i)^-1;
        q := ShallowCopy(GeneratorsOfGroup(G));
        q[p[1]] := Comm(q[p[2]]^-1,q[p[3]]^-1)*q[p[1]];
        Add(epi,GroupHomomorphismByImages(G,q));
        i := i+1;
            
        M[p[1]][p[3]][p[2]+n] := M[p[1]][p[2]][p[3]]^C[p[1]][p[2]];
        M[p[1]][p[2]][p[3]+n] := M[p[1]][p[3]][p[2]]^C[p[1]][p[3]];
            
        M[p[1]][p[3]+n][p[2]+n] := M[p[1]][p[2]][p[3]+n]^C[p[1]][p[2]];
        M[p[1]][p[2]+n][p[3]+n] := M[p[1]][p[3]][p[2]+n]^C[p[1]][p[3]];
            
        M[p[1]][p[3]+n][p[2]] := M[p[1]][p[2]][p[3]]^C[p[1]][p[3]];
        M[p[1]][p[2]+n][p[3]] := M[p[1]][p[3]][p[2]]^C[p[1]][p[2]];
        
        for s in [0,n] do for t in [0,n] do
            M[p[1]+n][p[2]+s][p[3]+t] := Comm(C[p[1]][p[2]+s]^-1,C[p[1]][p[3]+t]^-1) / M[p[1]][p[2]+s][p[3]+t];            
            M[p[1]+n][p[3]+s][p[2]+t] := Comm(C[p[1]][p[3]+s]^-1,C[p[1]][p[2]+t]^-1) / M[p[1]][p[3]+s][p[2]+t];            
        od; od;
    od;
    
    rels := [];
    
    # R0: M(x_a^alpha,[x_b^beta,x_c^gamma]) * M(x_a^alpha,[x_c^gamma,x_b^beta])
    # not necessary anymore, since we put only half the generators
    if true then
    for p in Arrangements([1..n],3) do
        for s in Tuples([0,n],3) do
            Add(rels,M[p[1]+s[1]][p[2]+s[2]][p[3]+s[3]]*M[p[1]+s[1]][p[3]+s[3]][p[2]+s[2]]);
        od;
    od;
    fi;
    
    # R1: [C(x_a,x_b),C(x_c,x_d)]
    for p in Arrangements([1..n],2) do
        if p<>[1,2] then continue; fi;
        for q in Arrangements([1..n],2) do
            if p[1]<>q[1] and p[1]<>q[2] and p[2]<>q[1] then
                Add(rels,Comm(C[p[1]][p[2]],C[q[1]][q[2]]));
            fi;
        od;
    od;
    
    # R2: [M(x_a^alpha,[x_b^beta,x_c^gamma]),M(x_d^delta,[x_e^epsilon,x_f^zeta])]
    for p in Arrangements([1..n],3) do for s in Tuples([0,n],3) do
        if p{[1,2]}<>[1,2] then continue; fi;
        for q in Arrangements([1..n],3) do for t in Tuples([0,n],3) do
            if q[2]>q[3] then continue; fi;
            if p[1]+s[1]<>q[1]+t[1] and not p[1] in q{[2,3]} and not q[1] in p{[2,3]} then
                Add(rels,Comm(M[p[1]+s[1]][p[2]+s[2]][p[3]+s[3]],M[q[1]+t[1]][q[2]+t[2]][q[3]+t[3]]));
            fi;    
        od; od;
    od; od;
    
    # R3: [C(x_a,x_b),M(x_c^gamma,[x_d^delta,x_e^epsilon])]
    for p in Arrangements([1..n],2) do
        if p<>[1,2] then continue; fi;
        for q in Arrangements([1..n],3) do for t in Tuples([0,n],3) do
            if not p[1] in q and not q[1] in p then
                Add(rels,Comm(C[p[1]][p[2]],M[q[1]+t[1]][q[2]+t[2]][q[3]+t[3]]));
            fi;
        od; od;
    od;
    
    # R4: [C(x_c,x_b)*C(x_a,x_b),C(x_c,x_a)]
    for p in Arrangements([1..n],3) do
        if p{[1,2]}<>[1,2] then continue; fi;
        Add(rels,Comm(C[p[3]][p[2]]*C[p[1]][p[2]],C[p[3]][p[1]]));
    od;
    
    # R5: M(x_a^alpha,[x_b^beta,x_c^gamma])^C(x_a,x_b^beta) / M(x_a^alpha,[x_c^gamma,x_b^-beta])
    # not necessary anymore, since we put only a quarter of the generators
    if true then
    for p in Arrangements([1..n],3) do for s in Tuples([0,n],3) do
        if p{[1,2]}<>[1,2] then continue; fi;
        Add(rels,M[p[1]+s[1]][p[2]+s[2]][p[3]+s[3]]^C[p[1]][p[2]+s[2]]/M[p[1]+s[1]][p[3]+s[3]][p[2]+n-s[2]]);
    od; od;
    fi;

    # R6: M(x_a^-alpha,[x_b^beta,x_c^gamma])*M(x_a^alpha,[x_b^beta,x_c^gamma]) / [C(x_a,x_c^gamma)^-1,C(x_a,x_b^beta)^-1]
    for p in Arrangements([1..n],3) do for s in Tuples([0,n],3) do
        if p{[1,2]}<>[1,2] then continue; fi;
        Add(rels,M[p[1]+n-s[1]][p[2]+s[2]][p[3]+s[3]]*M[p[1]+s[1]][p[2]+s[2]][p[3]+s[3]]/Comm(C[p[1]][p[2]+s[2]]^-1,C[p[1]][p[3]+s[3]]^-1));
    od; od;
    
    # R7: [C(x_a,x_b^beta)^-1,M(x_a^-alpha,[x_b^beta,x_c^gamma])] / [C(x_a,x_d^delta)^-1,C(x_a,x_c^gamma)^-1]
    for p in Arrangements([1..n],4) do for s in Tuples([0,n],4) do
        if p{[1,2]}<>[1,2] then continue; fi;
        Add(rels,Comm(C[p[1]][p[2]+s[2]]^-1,M[p[2]+s[2]][p[3]+s[3]][p[4]+s[4]]^-1)/Comm(C[p[1]][p[3]+s[3]]^-1,C[p[1]][p[4]+s[4]]^-1));
    od; od;
    
    # R8: M(x_a^alpha,[x_c^gamma,x_b^beta])*M(x_d^delta,[x_a^alpha,x_e^epsilon])*M(x_a^alpha,[x_b^beta,x_c^gamma])/M(x_d^delta,[x_c^gamma,x_b^beta])^C(x_d,x_e^-epsilon)/M(x_d^delta,[x_a^alpha,x_e^epsilon])/M(x_d^delta,[x_b^beta,x_c^gamma])
    for p in Arrangements([1..n],4) do for q in [1..n] do for s in Tuples([0,n],5) do p[5] := q;
        if p{[1,2]}<>[1,2] then continue; fi;
        if p[5] in p{[1,4]} then continue; fi;
        t := C[p[4]][p[5]]; if s[5]=n then t := t^-1; fi;
        Add(rels,M[p[1]+s[1]][p[3]+s[3]][p[2]+s[2]]*M[p[4]+s[4]][p[1]+s[1]][p[5]+s[5]]*
            M[p[1]+s[1]][p[2]+s[2]][p[3]+s[3]]/M[p[4]+s[4]][p[3]+s[3]][p[2]+s[2]]^C[p[4]][p[5]+n-s[5]]/M[p[4]+s[4]][p[1]+s[1]][p[5]+s[5]]/M[p[4]+s[4]][p[2]+s[2]][p[3]+s[3]]);
    od; od; od;
    
    # R9: M(x_c^gamma,[x_a^alpha,x_b^beta])^-C(x_a,x_b^beta) * M(x_c^gamma,[x_b^beta,x_a^alpha])*M(x_c^gamma,x[x_a^alpha,x_d^delta])*M(x_c^gamma,[x_a^alpha,x_b^beta])^-C(x_c,x_d^delta)
    for p in Arrangements([1..n],3) do for q in [1..n] do for s in Tuples([0,n],4) do p[4] := q;
        if p{[1,2]}<>[1,2] then continue; fi;
        if p[4] in p{[1,3]} then continue; fi;
        Add(rels,M[p[3]+s[3]][p[2]+s[2]][p[1]+s[1]]*M[p[3]+s[3]][p[1]+s[1]][p[4]+s[4]]*
            M[p[3]+s[3]][p[1]+s[1]][p[2]+s[2]]^C[p[3]][p[4]+n-s[4]]/M[p[3]+s[3]][p[1]+s[1]][p[4]+s[4]]^C[p[1]][p[2]+s[2]]);
    od; od; od;
    
    endos := [];
    Gendos := [];
    # I_1
    t := []; u := [];
    for q in Arrangements([1..n],2) do
        Add(t,C[q[1]][q[2]]);
        if 1=q[2] then Add(u,C[q[1]][q[2]]^-1); else Add(u,C[q[1]][q[2]]); fi;
    od;
    for q in Arrangements([1..n],3) do for s in Tuples([0,n],3) do
        if q[2]>q[3] or s<>[0,0,0] then continue; fi;
        Add(t,M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]);
        if 1 in q then s[Position(q,1)] := n-s[Position(q,1)]; fi;
        Add(u,M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]);
    od; od;
    Add(endos,GroupHomomorphismByImages(F,t,u));
    t := ShallowCopy(GeneratorsOfGroup(G));
    t[1] := t[1]^-1;
    Add(Gendos,GroupHomomorphismByImages(G,t));
    
    # P_s for all permutations s on {1..n}
    for p in GeneratorsOfGroup(SymmetricGroup(n)) do
        t := []; u := [];
        for q in Arrangements([1..n],2) do
            Add(t,C[q[1]][q[2]]);
            Add(u,C[q[1]^p][q[2]^p]);
        od;
        for q in Arrangements([1..n],3) do for s in Tuples([0,n],3) do
            if q[2]>q[3] then continue; fi;
            Add(t,M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]);
            Add(u,M[q[1]^p+s[1]][q[2]^p+s[2]][q[3]^p+s[3]]);
        od; od;
        Add(endos,GroupHomomorphismByImages(F,t,u));
        Add(Gendos,GroupHomomorphismByImages(G,Permuted(GeneratorsOfGroup(G),p^-1)));
    od;
    
    # M_{x_1^alpha,x_2^beta}
    for p in Tuples([0,n],2) do
        if p[1]=0 then alpha := 1; else alpha := -1; fi;
        t := []; u := [];
        for q in Arrangements([1..n],2) do
            Add(t,C[q[1]][q[2]]);
            if q[2]=1 and q[1]<>2 then # C(x_c,x_a)
                Add(u,(C[q[1]][2+p[2]]*C[q[1]][1+p[1]])^alpha);
            elif q[1]=1 and q[2]<>2 then # C(x_a,x_c)
                Add(u,M[1+p[1]][2+n-p[2]][q[2]]*C[1][q[2]]);
            elif q[1]=2 and q[2]<>1 then # C(x_b,x_c)
                Add(u,M[1+p[1]][2+n-p[2]][q[2]+n]*C[2][q[2]]);
            elif q=[2,1] then # C(x_b,x_a)
                Add(u,(C[2][1+p[1]]*C[1][2+p[2]])^alpha);
            else
                Add(u,C[q[1]][q[2]]);
            fi;
        od;
        for q in Arrangements([1..n],3) do for s in Tuples([0,n],3) do
            if q[2]>q[3] or s<>[0,0,0] then continue; fi;
            Add(t,M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]);
            if q[1]+s[1]=1+p[1] and not 2 in q then # M(x_a^alpha,[x_c^gamma,x_d^delta])
                Add(u,M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]^C[1][2+p[2]]);
            elif q[2]+s[2]=1+p[1] and not 2 in q then # M(x_c^gamma,[x_a^alpha,x_d^delta])
                Add(u,M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]^C[q[1]][2+n-p[2]]*M[q[1]+s[1]][2+p[2]][q[3]+s[3]]);
            elif q[2]+s[2]=1+n-p[1] and not 2 in q then # M(x_c^gamma,[x_a^-alpha,x_d^delta])
                Add(u,M[q[1]+s[1]][2+n-p[2]][q[3]+s[3]]^(C[q[1]][1]^alpha)*M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]);
            elif q[1]+s[1]=2+p[2] and not 1 in q then # M(x_b^beta,[x_c^gamma,x_d^delta])
                Add(u,(M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]*M[1+n-p[1]][q[2]+s[2]][q[3]+s[3]])^C[1][2+p[2]]);
            elif q[1]+s[1]=2+n-p[2] and not 1 in q then # M(x_b^-beta,[x_c^gamma,x_d^delta])
                Add(u,M[2+n-p[2]][q[2]+s[2]][q[3]+s[3]]*M[1+p[1]][q[2]+s[2]][q[3]+s[3]]);
            elif q[1]+s[1]=1+p[1] and q[2]+s[2]=2+p[2] then # M(x_a^alpha,[x_b^beta,x_c^gamma])
                Add(u,M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]^C[1][2+p[2]]);
            elif q[1]+s[1]=1+p[1] and q[2]+s[2]=2+n-p[2] then # M(x_a^alpha,[x_b^-beta,x_c^gamma])
                Add(u,M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]^C[1][2+p[2]]);
            elif q[1]+s[1]=2+p[2] and q[2]+s[2]=1+p[1] then # M(x_b^beta,[x_a^alpha,x_c^gamma])
                Add(u,M[q[1]+n-s[1]][q[2]+s[2]][q[3]+n-s[3]]*C[2][q[3]+n-s[3]]*M[q[2]+s[2]][q[1]+n-s[1]][q[3]+s[3]]*C[1][q[3]+s[3]]);
            elif q[1]+s[1]=2+p[2] and q[2]+s[2]=1+n-p[1] then # M(x_b^beta,[x_a^-alpha,x_c^gamma])
                Add(u,(C[1][q[3]+n-s[3]]*M[1+p[1]][q[3]+s[3]][2+n-p[2]]*C[2][q[3]+s[3]]*M[2+n-p[2]][q[3]+n-s[3]][1+p[1]])^(C[q[3]][1+n-p[1]]*C[q[3]][2+n-p[2]]));
            elif q[1]+s[1]=2+n-p[2] and q[2]+s[2]=1+p[1] then # M(x_b^-beta,[x_a^alpha,x_c^gamma])
                Add(u,((C[2][q[3]+s[3]]*M[q[2]+s[2]][q[3]+s[3]][q[1]+s[1]])^C[q[3]][2+p[2]]*M[q[1]+s[1]][q[3]+s[3]][q[2]+n-s[2]])^C[q[3]][1+p[1]]*C[1][q[3]+n-s[3]]);
            elif q[1]+s[1]=2+n-p[2] and q[2]+s[2]=1+n-p[1] then # M(x_b^-beta,[x_a^-alpha,x_c^gamma])
                Add(u,(C[1][q[3]+s[3]]^C[q[3]][1+n-p[1]]*M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]])^C[q[3]][2+n-p[2]]*M[1+p[1]][q[1]+s[1]][q[3]+s[3]]*C[2][q[3]+n-s[3]]);
            elif q[2]+s[2]=1+p[1] and q[3]+s[3]=2+p[2] then # M(x_c^gamma,[x_a^alpha,x_b^beta])
                Add(u,M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]^C[1][2+p[2]]);
            elif q[2]+s[2]=1+p[1] and q[3]+s[3]=2+n-p[2] then # M(x_c^gamma,[x_a^alpha,x_b^-beta])
                Add(u,M[q[1]+s[1]][q[3]+n-s[3]][q[2]+s[2]]);
            else
                Add(u,M[q[1]+s[1]][q[2]+s[2]][q[3]+s[3]]);
            fi;
        od; od;
        Add(endos,GroupHomomorphismByImages(F,t,u));
        u := ShallowCopy(GeneratorsOfGroup(G));
        v := ShallowCopy(GeneratorsOfGroup(G));
        if p[2]=0 then
            u[1] := (u[2]*u[1]^alpha)^alpha;
        else
            u[1] := (u[2]^-1*u[1]^alpha)^alpha;
        fi;
        Add(Gendos,GroupHomomorphismByImages(G,u));
    od;
    F := LPresentedGroup(F,[],endos,rels);
    F!.C := C; # hack: provide access to C and M generators as convenient tables
    F!.M := M;
    F!.Gendos := Gendos; # automorphisms of G such that endos[i] acts on Aut(G) by conjugation by Gendos[i]
    return GroupHomomorphismByImagesNC(F,A,epi);
end);