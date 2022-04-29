from hashlib import md5
import numpy as np

key_block_num = 0
key_space = 20
block_size = 2 ** key_space
start_val = key_block_num * block_size 
end_val = (key_block_num + 1) * block_size
roll_T = "0421312015"
matchstr = "00015"
success_resp = b'SCS'

marray = np.arange(start_val, end_val)
marray = marray.astype(str)
marray = np.char.zfill(marray, 10)

tarray = np.char.add(roll_T, marray)

earray = np.char.encode(tarray)
vec = lambda t: md5(t).hexdigest()
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