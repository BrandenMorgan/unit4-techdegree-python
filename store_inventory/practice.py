import csv
import datetime

# inventory_list = []
# with open('inventory.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         inventory_list.append(dict(row))
#
# for product in inventory_list:
#     product['product_price'] = int(product['product_price'].replace('$', '').replace('.', ''))
#     product['product_quantity'] = int(product['product_quantity'])
#     product['date_updated'] = datetime.datetime.strptime(product['date_updated'], '%m/%d/%Y')
#
#
# def backup_table(cls, csvfile):
#         """
#         Create a schema less backup of this model in a csv file.
#         """
#         query = cls.select()
#         if csvfile.tell():
#             desc = csvfile.fileno()
#             modified = datetime.fromtimestamp(os.path.getmtime(desc))
#             query = query.where(cls.modified > modified)
#         writer = csv.writer(csvfile)
#         writer.writerows(query.naive().tuples())
#
#         with open('test.csv', 'a+') as csvfile:
#         Entry.backup_table(csvfile)
# product_price = input('How much does each cost? -> $')
# # if no decimal entered add '00' to the end of integer. ie 1 -> 100 cents
# if '.' not in product_price:
#     product_price = product_price + '00'
# elif '.' in product_price:
#     product_price = product_price.replace('.', '')
#
# print(product_price)

current_date = datetime.datetime.strptime('01/08/2015','%d/%m/%Y').date()

print(current_date)
now = datetime.datetime.now()
print(now.strftime('%d/%m/%Y'))
