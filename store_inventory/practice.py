import csv
import datetime

inventory_list = []
with open('inventory.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        inventory_list.append(dict(row))



for product in inventory_list:
    product['product_price'] = int(product['product_price'].replace('$', '').replace('.', ''))
    product['product_quantity'] = int(product['product_quantity'])
    product['date_updated'] = datetime.datetime.strptime(product['date_updated'], '%m/%d/%Y')

print(inventory_list)
