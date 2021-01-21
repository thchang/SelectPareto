# Import the wrapped Fortran code (should automagically compile
#  on MacOS and Ubuntu with gfortran installed).
import fast_sort


# Create a large random valued array (and make copies).
import numpy as np
a = np.asarray(np.random.random(size=(10000,)), dtype=float)
b = a.copy()
i = np.asarray(np.arange(len(a)), dtype=int)
j = i.copy()


# Track the time of both methods.
import time


# Argsort an array with Fortran.
start = time.time()
fast_sort.argsort_r64(a, i)
end = time.time()
print("fortran: ",end-start)

#  re-sort
start = time.time()
fast_sort.argsort_r64(a, i)
end = time.time()
print("         ",end-start)


# Argsort the same array with numpy.
start = time.time()
j = np.argsort(b)
end = time.time()
b = b[j] # make 'b' sorted
print("numpy:   ",end-start)

#  re-sort
start = time.time()
_ = np.argsort(b)
end = time.time()
print("         ",end-start)


# Verify correctness.
try:    assert np.all(i == j)
except: print("ERROR: Number of bad indices:", np.sum(np.abs(i-j) > 0))
try:    assert np.all(a == b)
except: print("ERROR: Number of bad values: ", np.sum(np.abs(a-b) > 0))

