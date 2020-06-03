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
        print("\nEnter 'q' to quit.\n")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        try:
            choice = input('\nAction: ').lower().strip()
            if choice not in menu and choice != 'q':
                raise ValueError
            if choice in menu:
                clear()
                menu[choice]()
        except ValueError:
            print("\nYou must choose an option from the menu. 'v' 'a' or 'b'.\n")




def view_product():
    """View product by id"""
    while True:
        try:
            id = input("Enter the product id that you would like to view. > ")
            if not id.isnumeric() or id == '0':
                raise IndexError
            products = Product.select().where(Product.product_id == id)
            if int(id) > Product.select().count():
                raise IndexError
            for product in products:
                if str(product.product_price)[-2:] == '00' or len(str(product.product_price)) >= 3 :
                    product.product_price = str(product.product_price)[:-2] + '.' + str(product.product_price)[-2:]
                elif len(str(product.product_price)) < 3:
                     product.product_price = str(product.product_price)[:-1] + '.' + str(product.product_price)[-1:] + '0'


                print('\n' + 'Product: ' + product.product_name, '\nQuantity:', product.product_quantity,
                        '\nPrice: ' + '$', product.product_price, '\nDate added: ', product.date_updated.date().strftime('%m/%d/%Y'), '\n')
                print('p) view another product')
                print('q) return to main menu')

            next_action = input('\nAction: ').lower().strip()
            if next_action == 'p':
                continue
            if next_action == 'q':
                break
        except IndexError:
            print("Product of id '{}' not in database. Please enter valid id.\n".format(id))



def add_product():
    """Add a product"""
    while True:
        try:
            product_name = input('What is the name of the product you would like to add? -> ').title()
            if not product_name.isalnum():
                raise TypeError
            product_quantity = input('How many would you like to add? -> ')
            if not product_quantity.isnumeric():
                raise TypeError
            product_price = input('How much does each {} cost? -> $'.format(product_name))
            if '.' not in product_price and not product_price.isnumeric():
                raise TypeError
            if '.' not in product_price:
                product_price = product_price + '00'
            elif '.' in product_price:
                product_price = product_price.replace('.', '')
            add_to_database = input('Add this product to the database? [Yn] ').lower()
            if add_to_database in ['n', 'no']:
                break
            if add_to_database in ['y', 'yes']:
                try:
                    Product.create(product_name=product_name,
                                    product_quantity=product_quantity,
                                    product_price=int(product_price))
                    print('\Product added successfully!')
                    break
                except IntegrityError:
                    print('{} already exists in the database. Please enter a different product'.format(product_name))
                    product_record = Product.get(product_name=product['product_name'])
                    product_record.product_quantity = product['product_quantity']
                    product_record.product_price = product['product_price']
                    product_record.date_updated = product['date_updated']
                    product_record.save()
                    add_product = input('Would you like to add a product? [y]es/[n]o ').lower()
                    if add_product in ['y', 'yes']:
                        continue
                    else:
                        break
        except TypeError:
            print("Please make a valid entry.")

def backup():
    """Back up database"""
    with open('backup.csv', 'w', newline='') as csvfile:
        productwriter = csv.writer(csvfile)
        products = Product.select(Product.product_name, Product.product_price,
                                Product.product_quantity, Product.date_updated)
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
