_id = 0
class Node(object):
	def __init__(self, data):
		global _id
		self._id = _id
		_id += 1
		self.data = data
		self._next = None
	
	def append(self, data):
		self._next = Node(data)
		return self
	
	def next(self):
		return self._next

	def set_next(self, _next):
		self._next = _next
		return self
	
	def __repr__(self):
		return str(self._id) + ':'+ str(self.data)

	def __str__(self):
		return str(self._id) + ':' + str(self.data)

	def __eq__(self, other):
		return other is not None and self.data == other.data

class LinkedList(object):
	def __init__(self):
		self.head = None
		self._ptr = None
		self._ptr_prev = None
		self._len = 0

	def __iter__(self):
		self._ptr_prev = None
		self._ptr = self.head
		return self
	
	def __len__(self):
		return self._len

	def next(self):
		_start = self._ptr
		_prev = self._ptr_prev

		if self._ptr is None:
			raise StopIteration
		
		self._prev = self._ptr
		self._ptr = self._ptr.next()

		return (_prev, _start)

	def add(self, data, to_front=False):
		self._len += 1
		if self.head is None:
			self.head = Node(data)
			return self
		
		if to_front:
			self.head = Node(data).set_next(self.head)
			return self
		
		current = None
		for (prev,current) in self:
			pass

		current.append(data)
		return self

	def delete(self, data):
		''' deletes all nodes where node.data == data '''
		''' if you find a data node, set found.next = current when current.data != data'''
		detach = None

		for (previous, current) in self:
			if detach is not None:
				self._len-=1
				if current is None or current.data != data:
					detach.set_next(current)
					detach = None
				continue

			detach = None if current.data != data else self.head if previous == None else previous


	def dedupe(self):
		items = {}
		current = self.head
		previous = None
		while current:
			if current.data in items:
				if previous == None:
					self.head = current.next()
				else:
					previous.set_next(current.next())
			else:
				items[current.data] = None
			previous = current
			current = current.next()
		return self

	def __str__(self):
		current = self.head
		s = ''
		while current:
			s += str(current.data) + ","
			current = current.next()
		return s

class NumberList(LinkedList):
	def __init__(self, num):
		super(NumberList, self).__init__()
		rem = num
		while rem > 0:
			r = rem % 10
			self.add(r)
			rem = (rem - r) / 10

	def __add__(self, num):
		if isinstance(num, NumberList):
			t = 1
			total = 0
			


		else:
			self.__add__(NumberList(num))
	
	def __radd__(self, num):
		return self.__add__(num)

	def test(self):
		print next(self)
# x = LinkedList().add(5).add(6).add(6).add(3).add(5).add(2)

# print x, len(x)

# x.delete(6)
# x.delete(2)
# x.dedupe()
# for i in x:
	# print i
# print x, len(x)
x = NumberList(1234560)
# print x
x.test()