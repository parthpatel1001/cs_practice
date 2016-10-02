import random
import operator

def quick_sort(a, lo=0, hi=None, reverse=False):
	if hi is None:
		hi = len(a) - 1

	op = operator.ge if reverse else operator.le
	
	if lo <= hi:
		p = partition(a, lo, hi, op)
		quick_sort(a, lo, p - 1, reverse)
		quick_sort(a, p+1, hi, reverse)

def partition(a, lo, hi, op):
	pivot = a[hi]
	i = lo
	for j in range(lo, hi):
		if op(a[j], pivot):
			a[i], a[j] = a[j], a[i]
			i += 1
	a[i], a[hi] = a[hi], a[i]
	return i

for i in range(1,100):
	x = [i for i in range(1,10)]
	y = sorted(list(x))
	random.shuffle(x)
	quick_sort(x)
	if x != y:
		print 'Error',x,y
print 'Passed'