#1
def generat(n):
    nov=1
    while nov <= n:
        yield nov
        nov += 1

n= int(input())
for num in generat(n):
    print(num**2)


#2

def evens(num):
     cur=0
     while cur <= num:
          if (cur % 2 == 0):
               yield cur
          cur +=1

numb = int(input())
ev = evens(numb)
res=[str(i) for i in ev]

print(",".join(res))


#3
def divis(num):
     cur=0
     while cur <= num:
          if (cur % 3 == 0 and cur % 4==0):
               yield cur
          cur +=1

numb = int(input())
div = divis(numb)
res=[str(i) for i in div]

print(" ".join(res))



#4

def squares(a,b):
    for i in range(a,b):
        yield i**2
    
numbrs = [int(x) for x in input().split()]

firs= numbrs[0]
secn= numbrs[1]

for i in squares(firs,secn):
    print(i, end=" ")

#5

def down(n):
    nex = n
    while nex >= 0:
        yield nex
        nex -=1


start = int(input())
for i in down(start):
    print(i , end = " ")
