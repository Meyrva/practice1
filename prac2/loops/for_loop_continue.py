#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)
#2
for x in range(6):
  if x == 3: continue
  print(x)
else:
  print("Finally finished!")