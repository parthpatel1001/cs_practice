from profile import profile
from random import shuffle

def merge_sort(items):
	if len(items) == 1:
		return items
	result = []

	midpoint = len(items) / 2
	left = merge_sort(items[0:midpoint])
	right = merge_sort(items[midpoint:])
	leftlen = len(left)
	rightlen = len(right)

	i = j = 0

	while i < leftlen and j < rightlen:
		if left[i] < right[j]:
			result.append(left[i])
			i+=1
		else:
			result.append(right[j])
			j+=1

	return result + left[i:] + right[j:]

def merge_sort_2(items):
	l = len(items)
	if l <= 1:
		return items

	midpoint = l / 2
	left = merge_sort(items[0:midpoint])
	right = merge_sort(items[midpoint:])
	llen = len(left)
	rlen = len(right)
	i = j = 0

	while i < llen and j < rlen:
		lpiece = left[i]
		rpiece = right[j]
		if lpiece < rpiece:
			items[i+j] = lpiece
			i+=1
		else:
			items[i+j] = rpiece
			j+=1
	
	if i < llen:
		while i < llen:
			items[i+j] = left[i]
			i+=1
	else:
		while j < rlen:
			items[i+j] = right[j]
			j+=1
	
	return items




@profile
def test_merge_sort(items,expected):
	result = merge_sort(items,)
	if result != expected:
		print '\t',False

@profile
def test_merge_sort_2(items,expected):
	result = merge_sort_2(items)
	if result != expected:
		print '\t',False

for i in range(1,8):
	print 10,'^',i
	a = 10 ** i
	x = range(1,a)
	y = range(1,a)
	shuffle(x)
	shuffle(y)
	test_merge_sort(x, sorted(list(x)))
	test_merge_sort_2(y, sorted(list(y)))



