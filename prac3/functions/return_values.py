#1
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)
#2
def get_greeting():
  return "Hello from a function"

print(get_greeting())
#3
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))
