#1
#Logical operators are used to combine conditional statements:
x = 5

print(1 < x < 10)

print(1 < x and x < 10)
#2
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y)
#3
x = 5

print(x < 5 or x > 10)
#4
x = 5

print(not(x > 3 and x < 10))
#5
x = [1, 2, 3]
y = [1, 2, 3]

print(x == y)
print(x is y)