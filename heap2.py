import operator
from random import randint

def heapify(items, i, l, op=operator.gt):
	'''default max_heapify'''
	s = (l / 2) - 1
	while i <= s:
		left = 2 * i  + 1
		right = left + 1
		swap = i
		if left < l and op(items[left], items[swap]):
			swap = left
		if right < l and op(items[right], items[swap]):
			swap = right
		if swap != i:
			items[i], items[swap], i = items[swap], items[i], swap
		else:
			return

def build_heap(items, op=operator.gt):
	'''default builds max heap'''
	l = len(items)
	i = (l / 2) - 1
	while i >= 0:
		heapify(items, i, l, op)
		i-=1

def heap_sort(items, reverse=False):
	op = operator.lt if reverse else operator.gt
	build_heap(items, op)
	l = len(items) - 1
	while l > 0:
		items[0], items[l] = items[l], items[0]
		l-=1
		heapify(items, 0, l, op)

x = [randint(1,10) for _ in xrange(1,20)]
y = sorted(list(x))

heap_sort(x)

print x == y, x, y
x = []
heap_sort(x)
print x

x = [1]
heap_sort(x)
print x

x = [2,1]
heap_sort(x)
print x
