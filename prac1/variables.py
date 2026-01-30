#1
x,y,z= "me", 5 , "you"
print(x,y,z)
#2
a=3
a="you"
print(a)
#3
i, o, p = "Orange", "Banana", "Cherry"
print(i)
print(o)
print(p)
#4
f=c=h="Love"
print(f)
print(c)
print(h)
#5
d="good"
def myfunc():
    global d
    d="not bad"
myfunc()

print("The Sims is "+ d )

