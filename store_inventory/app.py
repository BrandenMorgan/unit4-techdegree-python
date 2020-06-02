from collections import OrderedDict
import csv
import datetime
import os
import sys

from peewee import *


db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = IntegerField(primary_key=True)
    product_name = CharField(max_length=255, unique=True)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(null=False)
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


inventory_list = []
with open('inventory.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        inventory_list.append(dict(row))

for product in inventory_list:
    product['product_price'] = int(product['product_price'].replace('$', '').replace('.', ''))
    product['product_quantity'] = int(product['product_quantity'])
    product['date_updated'] = datetime.datetime.strptime(product['date_updated'], '%m/%d/%Y')


def add_to_database(**kwargs):
    for product in inventory_list:
        try:
            Product.create(**product)

        except IntegrityError:
            product_record = Product.get(product_name=product['product_name'])
            product_record.product_quantity = product['product_quantity']
            product_record.product_price = product['product_price']
            product_record.date_updated = product['date_updated']
            product_record.save()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    choice = None

    while choice != 'q':
        # clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        try:
            choice = input('Action: ').lower().strip()
            if choice not in menu and choice != 'q':
                raise ValueError
            if choice in menu:
                clear()
                menu[choice]()
        except ValueError:
            print("\nYou must choose an option from the menu. 'v' 'a' or 'b'.\n")



#strip_tz(date_str)
def view_product():
    """View product by id"""
    while True:
        try:
            id = input("Enter the product id that you would like to view. > ")
            products = Product.select().where(Product.product_id == id)
            if int(id) > Product.select().count():
                raise IndexError
            for product in products:
                print('\n' + 'Product: ', product.product_name, product.product_quantity,
                        product.product_price, product.date_updated, '\n')
                print('n) view another product')
                print('d) delete product')
                print('q) return to main menu')

            next_action = input('Action: [Ndq] ').lower().strip()
            if next_action == 'q':
                break
        except IndexError:
            print("Product of id {} not in database. Please try again. ".format(id))



def add_product():
    """Add a product"""
    product_name = input('What is the name of the product you would like to add? -> ')
    product_quantity = input('How many would you like to add? -> ')
    product_price = int(input('How much does each {} cost? -> $'.format(product_name)).replace('.', ''))

    if input('Add this product to the database? [Yn] ').lower != 'n':
        Product.create(product_name=product_name,
                        product_quantity=product_quantity,
                        product_price=product_price)
        print('Product added successfully!')


# backs up with product_id but has no fieldname
def backup():
    """Back up database"""
    with open('backup.csv', 'w', newline='') as csvfile:
        productwriter = csv.writer(csvfile)
        products = Product.select()
        productwriter.writerow(product.keys())
        productwriter.writerows(products.tuples())


menu = OrderedDict([
    ('v', view_product),
    ('a', add_product),
    ('b', backup),
])


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    add_to_database(product_name=product['product_name'],
                    product_quantity=product['product_quantity'],
                    product_price=product['product_price'],
                    date_updated=product['date_updated'])
    menu_loop()
