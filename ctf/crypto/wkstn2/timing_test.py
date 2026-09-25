import time
src = open("beam_attack.py").read().split("BEAM_WIDTH = 12")[0]
exec(src)
t0 = time.time()
v = vote_for_byte((), 3, frames[:2000])
print("2000 frames one node:", time.time() - t0)
