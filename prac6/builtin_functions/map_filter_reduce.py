from functools import reduce
nums = [1,2,3,4,5,6]

sqr = list(map(lambda x: x**2, nums))

evens = list(filter(lambda x: x%2 == 0, nums))

prods = reduce(lambda x, y : x*y , nums)

print(sqr)
print(evens)
print(prods)