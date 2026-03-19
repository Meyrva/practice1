names = ['Alisa','Sam','Kris']
scores = [79,29,89]

for index, name in enumerate(names, start = 1):
    print(index, name)

for name, score in zip(names,scores):
    print(f'{name} have {score} points')

if isinstance(scores, list):
    print("It's a list")