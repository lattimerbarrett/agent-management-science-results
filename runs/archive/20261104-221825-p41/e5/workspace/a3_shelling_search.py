from pathlib import Path
p=Path('scratchpad.py').read_text()
p=p[:p.index('if __name__ == "__main__":
 start=time.time();data=prep(10,3)
 for seed in range(5000):
  a,b=trial(data,seed)
  if b:
   print("FOUND",seed,len(a),len(b),a,flush=True);break
 else:print("No stuck shelling in 5000 randomized trials, n=10,d=3;",time.time()-start,"seconds")
