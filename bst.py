from collections import deque
from random import randint

class Node(object):
	def __init__(self, key, data):
		self.key = key
		self.data = data
		self.left = None
		self.right = None
		self.parent = None
		self.subtree_height = 0

	def __repr__(self):
		return '%s %s %s' % (self.left if self.left is not None else '', self.key, self.right if self.right is not None else '')
	
	def __eq__(self, other):
		return isinstance(other, Node) and self.key == other.key

	def remove_child(self, node, replace_with=None):
		if self.left is not None and self.left.key == node.key:
			self.left = replace_with
		elif self.right is not None and self.right.key == node.key:
			self.right = replace_with
	
	def swap(self, other):
		self.key = other.key
		self.data = other.data

class BST(object):
	def __init__(self):
		self.root = None

	def insert(self, node):
		if not isinstance(node, Node):
			raise TypeError('node to inseret must be type Node not (%s)' % type(node))
		
		if self.root is None:
			self.root = node
			return self

		current = self.root

		while True:
			if node.key == current.key:
				break # probably more conventional to overright
			elif node.key < current.key:
				if current.left:
					current = current.left
				else:
					current.left = node
					node.parent = current
					break
			else:
				if current.right:
					current = current.right
				else:
					current.right = node
					node.parent = current
					break

		while current:
			current.subtree_height = max(current.left.subtree_height if current.left else 0, current.right.subtree_height if current.right else 0) + 1
			current = current.parent

		return self
	
	def delete(self, node):
		if not isinstance(node, Node):
			raise TypeError('node to inseret must be type Node not (%s)' % type(node))
		
		current = self.root
		found = False
		while current:
			if node.key == current.key:
				found = True
				if current.left is None and current.right is None:
					current.parent.remove_child(current)
					current = current.parent
				elif current.left is None:
					current.parent.remove_child(current, current.right)
				elif current.right is None:
					current.parent.remove_child(current, current.left)
				else:
					successor = current.right
					
					while successor.left:
						successor = successor.left
					print 'found successor', successor.key, 'parent', successor.parent.key, 'current', current.key,'current parent', current.parent.key
					successor.parent.remove_child(successor, successor.right)
					print 'removed child from parent, replaced with suc.right', successor.right.key if successor.right else '_'
					

				break
			elif node.key < current.key:
				current = current.left
			else: # >=
				current = current.right
		
		# if found:
		# 	while current:
		# 		current.subtree_height = max(current.subtree_height - 1, 0)


	def in_order_traverse(self, current=None):
		''' left, current, right '''
		if current is None:
			current = self.root
		
		if current.left is not None:
			for l in self.in_order_traverse(current.left):
				yield l
		
		yield current
		
		if current.right is not None:
			for r in self.in_order_traverse(current.right):
				yield r

	def pre_order_traverse(self, current=None):
		''' current, left, right '''
		if current is None:
			current = self.root

		yield current

		if current.left is not None:
			for l in self.pre_order_traverse(current.left):
				yield l

		if current.right is not None:
			for r in self.pre_order_traverse(current.right):
				yield r

	def post_order_traverse(self, current=None):
		'''left, right, current'''
		if current is None:
			current = self.root

		if current.left is not None:
			for l in self.post_order_traverse(current.left):
				yield l
		
		if current.right is not None:
			for r in self.post_order_traverse(current.right):
				yield r

		yield current
	
	def bread_first_traverse(self):
		q = deque()
		q.append((self.root, 0, 'root'))

		while q:
			c, l,d = q.popleft()
			yield c,l,d
			
			if c.left is not None:
				q.append((c.left,l+1,'L'))
			
			if c.right is not None:
				q.append((c.right,l+1,'R'))

	def pretty_print(self, item=None, level=0):
		if item == None:
			item = self.root

		if item.right is not None:
			self.pretty_print(item.right, level+1)
		
		if level != 0:
			out = ''
			for i in range(0, level):
				out += '|\t'
			print out + "|-------" + '%s (p:%s,sh:%s)'% (item.key, item.parent.key, item.subtree_height)
		else:
			print '%s (p:%s,sh:%s)'% (item.key, '_', item.subtree_height)
		
		if item.left is not None:
			self.pretty_print(item.left, level+1)
	
	def __repr__(self):
		pass

	

b = BST()
[b.insert(Node(randint(1,100),None)) for _ in range(1,5) ]
b.insert(Node(20,None))
[b.insert(Node(randint(1,100),None)) for _ in range(1,10)]

b.pretty_print()

print [i.key for i in b.in_order_traverse()]
b.delete(Node(20,None))
print
print

b.pretty_print()
print [i.key for i in b.in_order_traverse()]
'''
0 
1 
2 
3 
4 

			84
		  51, 94
		21, 52, 86
	  92, 80
	54



0 root 	84
1 L 	51
1 R 	94
2 L 	21
2 R 	52
2 L 	86
3 R 	80
3 R 	92
4 L 	54



'''