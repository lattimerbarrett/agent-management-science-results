import sys, json
sys.path.insert(0,'workspace')
from agent1_twin_cycle_engine import count_cycles
import networkx as nx
from math import factorial

def brute(G):
 ans=0
 for start in G:
  def dfs(path,used):
   nonlocal ans
   for w in G[path[-1]]:
    if w==start:
     if len(path)>=3:ans+=1
    elif w>start and w not in used:
     dfs(path+[w],used|{w})
  dfs([start],{start})
 return ans//2

def blow(sz,ad):
 G=nx.Graph();types=[]
 for i,k in enumerate(sz):types.extend([i]*k)
 G.add_nodes_from(range(len(types)))
 G.add_edges_from((i,j) for i in G for j in G if i<j and ad[types[i]][types[j]])
 return G

cases=[([4],[[1]]),([2,2],[[0,1],[1,1]]),([2,3,2],[[1,1,0],[1,0,1],[0,1,1]]),([1,2,2,1],[[0,1,0,1],[1,1,1,0],[0,1,0,1],[1,0,1,0]])]
for sz,ad in cases:
 a=count_cycles(sz,ad);b=brute(blow(sz,ad));assert a==b
 print(sz,a,b)
for row in json.load(open('workspace/agent1_r2_cycle_comparison.json')):
 print(row['n'],len(row['Q_cycles']),len(row['ext_cycles']))
from pathlib import Path
Path('workspace/agent1_twin_brute_verify.py').write_text(Path(__file__).read_text())
