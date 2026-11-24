import pickle
D=pickle.load(open('4mono.pkl','rb'))
for w in [272,288,296,304,308,312,314,316,318]:
 a=D[w];print(w,[(i,x) for i,x in enumerate(a) if x], 'free',a[15], 'ambient',sum(a)-a[0])
