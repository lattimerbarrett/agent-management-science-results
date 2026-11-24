import networkx as nx

def cut_edges(H,S):return [(u,v)for u,v in H.edges() if ((S>>u)&1)!=((S>>v)&1)]
def is_matching(E,n):
    ds=[0]*n
    for u,v in E:ds[u]+=1;ds[v]+=1
    return max(ds,default=0)<=1

def is_P3_forest(E,n):
    ds=[0]*n
    for u,v in E:ds[u]+=1;ds[v]+=1
    return max(ds,default=0)<=2 and all(not(ds[u]==ds[v]==2)for u,v in E)

if __name__=='__main__':
    pairs=0
    for H in nx.graph_atlas_g():
        n=len(H)
        if n>5:continue
        masks=[S for S in range(1<<n)if is_matching(cut_edges(H,S),n)]
        for S in masks:
            for T in masks:
                assert is_P3_forest(cut_edges(H,S&T),n)
                assert is_P3_forest(cut_edges(H,S|T),n)
                pairs+=1
    print('Verified matching-cut uncrossing on',pairs,'cut pairs across all graphs <=5 vertices.')
