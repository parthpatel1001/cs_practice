import math
import operator

class Heap(object):
	def __init__(self, heap=None, min_heap=False):
		self.heap = [0] + (heap if heap is not None else [])
		self.size = 0
		self.min_heap = min_heap

	def height(self):
		return int(math.ceil(math.log(self.size + 1,2)) - 1)

	def max_heapify(self, heap, i, min_heap=False):
		l = len(heap)
		s = l / 2
		op = operator.gt if min_heap else operator.lt
		print op
		while i < s:
			left = i * 2
			right = i * 2 + 1
			swap = i

			if op(heap[left], heap[i]):
				swap = left
			
			if right < l and op(heap[right], heap[swap]):
				swap = right

			if swap != i:
				heap[i], heap[swap], i = heap[swap], heap[i], swap
			else:
				return


	def build_max_heap(self, items):
		for i in range(len(items) / 2, 0, -1):
			max_heapify(items)
		

	def extract_root(self):
		root, self.heap[1] = self.heap[1], self.heap[self.size]
		del self.heap[self.size]
		self.size-=1
		self.max_heapify(self.heap, 1)

		return root

	def bubble_up(self, heap, i):
		'''bubble key i up to correct position'''
		parent = i / 2
		while parent > 0:
			if heap[i] > heap[parent]:
				break

			heap[i], heap[parent] = heap[parent], heap[i]
			i, parent = parent, parent / 2
	
	

	def insert(self, item):
		self.heap.append(item)
		self.size += 1
		self.bubble_up(self.heap, self.size)



h = Heap()
h.insert(10)
h.insert(12)
h.insert(14)
h.insert(8)
h.insert(6)
h.insert(4)
h.insert(3)

print h.heap, h.height(), Heap([10,12,14,8,6,4,3]).heap
'''
[0, 3, 8, 4, 12, 10, 14, 6]
      3
  8      4
12 10  14 6
'''
print h.extract_root(), h.heap, h.height()
'''
3 [0, 4, 8, 6, 12, 10, 14]

      4
  8       6
12 10    14
'''
