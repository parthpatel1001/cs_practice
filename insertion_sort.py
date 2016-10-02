# take current_item
# compare previous item
# if bigger, copy previous item to next spot
# repeat until first item, or item < current_item found
# put current_item in last copied spot
def insertion_sort(items):
	for j in xrange(1, len(items)):
		item = items[j]
		i = j - 1
		while i >= 0 and items[i] > item:
			items[i + 1] = items[i]
			i-=1
		items[i+1] = item



x = [4,1,9,81,14,531]
print x
y = sorted([4,1,9,81,14,531])

insertion_sort(x)

print x, y, x == y

