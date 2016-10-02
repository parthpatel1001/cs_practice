from random import randint
import operator
# https://en.wikipedia.org/wiki/Binary_heap
# https://en.wikipedia.org/wiki/Heapsort

def insert(heap, item, min_heap=False):
	op = operator.le if min_heap else operator.ge
	heap.append(item)
	i = len(heap)
	parent = i / 2
	while parent > 0:
		child = i - 1
		p_index = parent - 1
		if op(heap[p_index], heap[child]):
			return
		heap[child], heap[p_index] = heap[p_index], heap[child]
		i, parent = parent, parent / 2

def max_heapify(heap, i, l, op):
	s = l / 2
	while i <= s: # l / 2 + 1 are leaves
		left =  2 * i + 1
		right = 2 * i + 2
		swap = i

		if left < l and op(heap[left], heap[swap]):
			swap = left
		if right < l and op(heap[right], heap[swap]):
			swap = right

		if swap != i:
			heap[i], heap[swap], i = heap[swap], heap[i], swap
		else:
			return

def extract(heap, min_heap=False):
	rootItem, heap[0]= heap[0], heap.pop()
	op = operator.lt if min_heap else operator.gt
	max_heapify(heap, 0, len(heap), op)	
	return rootItem

def build_heap(items, min_heap=False):
	l = len(items)
	i = (l / 2) - 1
	op = operator.lt if min_heap else operator.gt
	while i >= 0:
		max_heapify(items, i, l, op)
		i-=1

def heap_sort(items, reverse=False):
	build_heap(items, min_heap=reverse)
	op = operator.lt if reverse else operator.gt
	l = len(items)
	while l > 0:
		l-=1
		items[0], items[l] = items[l], items[0]
		max_heapify(items, 0, l, op)


def valid_heap(heap, min_heap=False):
	l = len(heap)
	i = 0
	op = operator.lt if min_heap else operator.gt
	while i < l:
		left = 2 * i + 1
		right = 2 * i + 2

		if left < l and op(heap[left], heap[i]):
			return False, 'L(%s:%s) P(%s:%s)' %(left, heap[left], i, heap[i]), heap
		if right < l and op(heap[right], heap[i]):
			return False, 'R(%s:%s) P(%s:%s)' %(right, heap[right], i, heap[i]), heap
		i+=1
	return True, 

def test_max_heap_insert(times):
	for i in range(1,times):
		heap = []
		for i in range(1,10):
			insert(heap, randint(1,10))
		result = valid_heap(heap)
		if not result[0]:
			print 'FAILED: test_max_heap_insert', heap, result
			return
	print 'PASSED: test_max_heap_insert'

def test_min_heap_insert(times):
	for i in range(1,times):
		heap = []
		for i in range(1,10):
			insert(heap, randint(1,10), min_heap=True)
		result = valid_heap(heap, min_heap=True)
		if not result[0]:
			print 'FAILED: test_min_heap_insert', heap, result
			return
	print 'PASSED: test_min_heap_insert'

def test_max_heap_extract(times):
	for _ in range(1,times):
		heap = []
		for i in range(1,10):
			insert(heap, randint(1,100))
		expected = max(heap)
		result = extract(heap)
		if expected != result:
			print 'FAILED: test_max_heap_extract, invalid max', result, expected, heap
			return
		result = valid_heap(heap)
		if not result[0]:
			print 'FAILED: test_max_heap_extract, invalid max heap', result
			return
	print 'PASSED: test_max_heap_extract'

def test_min_heap_extract(times):
	for _ in range(1,times):
		heap = []
		for i in range(1,10):
			insert(heap, randint(1,100), min_heap=True)
		expected = min(heap)
		result = extract(heap, min_heap=True)
		if expected != result:
			print 'FAILED: test_min_heap_extract, invalid min', result, expected, heap
			return
		result = valid_heap(heap, min_heap=True)
		if not result[0]:
			print 'FAILED: test_min_heap_extract, invalid min heap', result
			return
	print 'PASSED: test_min_heap_extract'

def test_build_max_heap(times):
	for _ in range(1,times):
		for i in range(1,10):
			items = [randint(1,100) for i in range(1,10)]
			build_heap(items)
			result = valid_heap(items)
			if not result[0]:
				print 'FAILED: test_build_max_heap', result
				return
		
	print 'PASSED: test_build_max_heap'

def test_heap_sort_incr(times):
	for _ in range(1, times):
		for i in range(1,10):
			items = [randint(1,100) for _ in range(1,10)]
			expected = sorted(list(items))
			heap_sort(items)
			if items != expected:
				print 'FAILED: test_heap_sort_incr', items, expected
				return
	print 'PASSED: test_heap_sort_incr', items

def test_heap_sort_decr(times):
	for _ in range(1, times):
			items = [randint(1,100) for _ in range(1,10)]
			expected = sorted(list(items), reverse=True)
			heap_sort(items, reverse=True)
			if items != expected:
				print 'FAILED: test_heap_sort_decr', items, expected
				return
	print 'PASSED: test_heap_sort_decr', items


times=3000
test_min_heap_insert(times)
test_min_heap_insert(times)
test_max_heap_extract(times)
test_min_heap_extract(times)
test_build_max_heap(times)
test_heap_sort_incr(times)
test_heap_sort_decr(times)


