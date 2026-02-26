#1

import math
print("Input degree:", end=" ")
a = int(input())
print("Output radian:", round(math.radians(a), 6))

#2

print("Height:", end=" ")
h= int(input())

print("Base, first value:", end=" ")
f= int(input())

print("Base, second value:", end=" ")
s= int(input())

res= (math.fsum([f,s])/2)*h
print("Output:", res)
#3

print("Input number of sides:",end=" ")
num=float(input())

print("Input the length of a side:", end=" ")
leng=float(input())

area= (num* leng**2)/(4 * math.tan(math.pi/num))
print("The area of the polygon is:",int(area))


#4

print("Length of base:",end=" ")
l=float(input())

print("Height of parallelogram:", end=" ")
h=float(input())

res= (l,h)
print("Expected Output:",math.prod(res))
