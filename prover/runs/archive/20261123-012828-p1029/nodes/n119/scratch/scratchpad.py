import os
for root,ds,fs in os.walk('experiments/e1',followlinks=True):
    for f in fs:
        print(f)
