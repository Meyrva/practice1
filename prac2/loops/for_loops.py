#1

fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
#2

for x in "banana":
  print(x)
#3

for x in range(6):
  print(x)
#4

adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)
#5

for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")