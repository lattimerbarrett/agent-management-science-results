import sys,json,pathlib,collections,time
sys.path.insert(0,'workspace');from agent1_checked_grid import dyadic_blocks,truth_table;from agent3_lift_closure import veronese,closure
v=veronese(14,5);hist=collections.Counter();hits=[];count=0;t0=time.time()
for a in range(129):
 for b in range(129):
  delta=308-(128*(a+b)-2*a*b)
  if delta%128:continue
  t=delta//128;z=o=0
  for x0,x1,y0,y1,iszero in [(0,a,0,b,True),(a,128,b,128,True),(0,a,b,128,False),(a,128,0,b,False)]:
   s=sum(sx*sy//128 for x,sx in dyadic_blocks(x0,x1) for y,sy in dyadic_blocks(y0,y1) if sx*sy>=128)
   if iszero:z+=s
   else:o+=s
  if not -o<=t<=z:continue
  tt=truth_table(a,b,t);S=set(map(int,tt.nonzero()[0]));assert len(S)==308
  ex,rk=closure(S,v);hist[len(ex)]+=1;count+=1
  if ex:hits.append({'a':a,'b':b,'t':t,'support':sorted(S),'outside':[p for p,c in ex]})
print('count',count,'hist',hist,'hits',len(hits),'sec',time.time()-t0)
json.dump({'count':count,'hist':dict(hist),'hits':hits},open('workspace/agent2_grid308_cl5.json','w'));pathlib.Path('workspace/agent2_grid308_cl5.py').write_text(pathlib.Path(__file__).read_text())
