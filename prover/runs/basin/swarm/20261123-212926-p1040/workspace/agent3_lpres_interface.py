from sage.all import libgap

def lpres_source_layer(n,c):
    """Inspect installed LPRES source; NOT asserted equal to IA_n."""
    libgap.eval('LoadPackage("lpres" : OnlyNeeded := true)')
    for cmd in [f'F:=FreeGroup({n})','A:=AutomorphismGroup(F)',
                'e:=EmbeddingOfIASubgroup(A)','I:=Source(e)',
                f'Q:=NilpotentQuotient(I,{c})']:
        libgap.eval(cmd)
    return libgap.eval(f'AbelianInvariants(LowerCentralSeriesOfGroup(Q)[{c}])').sage()

if __name__=='__main__':
    from collections import Counter
    for c in range(1,4):
        print(c,dict(Counter(lpres_source_layer(3,c))))
