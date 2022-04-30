from hashlib import md5
import numpy as np

def vec(t):
    return md5(t).hexdigest()

key_block_num = 0
key_space = 22
block_size = 2 ** key_space
start_val = key_block_num * block_size 
end_val = (key_block_num + 1) * block_size
roll_T = "0421312015"
matchstr = "00015"
success_resp = b'SCS'
max_key_length = len(str(2**32))
# print(max_key_length)

marray = np.arange(start_val, end_val)
marray = marray.astype(str)
marray = np.char.zfill(marray, max_key_length)

tarray = np.char.add(roll_T, marray)

earray = np.char.encode(tarray)
# vec = lambda t: md5(t).hexdigest()
trun = np.vectorize(vec)
harray = trun(earray)
sharray = harray.astype('U5')

cmarray = np.char.equal(matchstr, sharray)
# print(cmarray)
resarray = harray[cmarray]
resarray = np.char.encode(resarray)
# print(resarray)
finarray = np.char.add(success_resp, resarray)
print(finarray)

for pkt in finarray:
    print(pkt)