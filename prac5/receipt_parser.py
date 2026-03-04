import re
import csv

#1 Extract all prices from the receipt
def prices(results):
    for result in results:
        price = result.group("price").strip()
        print(price)
        

#2 Find all product names
def prodnames(results):
    for result in results:
        names = result.group('name')
        print(names)


#3 Calculate total amount
def total(results):
    total_amount = 0.0

    for result in results:
        price = result.group("price").replace(",",".").replace(" ","").strip()
        total_amount += float(price)
    print(total_amount)


#4 Extract date and time information
def date(results,text):
    last = r"\n(?P<ficspris>.+):\n(?P<nums>[0-9]+)\n(?P<timeinfo>.+):\s*(?P<date>[0-9.]+)\s+(?P<time>[0-9:]+)"

    res = re.finditer(last, text)

    for t in res: 
        date, time = t.group("date","time")
        print(date, time)


#5 Find payment method
def payment(results,text):
    last = r"\n(?P<stoimos>[0-9]+)\n(?P<totall>.+)\n(?P<paiment>.+)\:\n(?P<summ>.+)\n"

    res = re.finditer(last, text)

    for time in res:
        t = time.group("price").strip()
        print(t)






file = open("raw.txt", "r", encoding="utf8")

text = file.read()
pattern = r"\n(?P<order>[0-9]+)\.\n(?P<name>.+)\n(?P<count>.+)x(?P<price>.+)\n"

results = re.finditer(pattern, text)

#1
prices(results)
#2
prodnames(results)
#3
total(results)
#4
date(results,text)
#5
payment(results,text)
#6 Create a structured output (JSON or formatted text)
with open('data.csv', "w", newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['order', 'name', 'count', 'price'])
    for x in results:
        writer.writerow([
            x.group('order'),
            x.group('name'),
            float(x.group('count').strip().replace(',', '.')),
            float(x.group('price').strip().replace(',', '.').replace(' ', ''))
        ])














