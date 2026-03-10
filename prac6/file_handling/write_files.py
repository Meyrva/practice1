with open("sample.txt", "a") as f:
    f.write("It's new line")

with open("sample.txt") as f:
    print(f.read())