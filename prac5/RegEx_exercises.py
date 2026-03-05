
import re

text_to_match = "Now let's abb the “Hello, everybody , it's me abbb“ page to the repository."

#1
print(re.findall(r"ab*", text_to_match))

#2
print(re.findall(r"ab{2,3}", text_to_match))

#3
print(re.findall(r"[a-z]+_[a-z]+", text_to_match))

#4
print(re.findall(r"[A-Z][a-z]+", text_to_match))

#5
print(re.findall(r"a.*b", text_to_match))

#6
print(re.sub(r"[ ,.]",":", text_to_match))

#7
snake = "snake_e_s"
print(re.sub(r'(?:^|_)(.)', lambda m: m.group(1).upper(), snake ))

#8
print(re.split(r"(!=[A-Z])", text_to_match))

#9
print(re.sub(r"(\w)([A-Z])", r"\1 \2", text_to_match))

#10
camel = "ExampleWord"
print(re.sub(r'(?<!^)(?=[A-Z])', '_', camel))