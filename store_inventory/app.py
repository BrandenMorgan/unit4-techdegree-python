import csv
import datetime
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




if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    #read in the csv
    #function to run app and user menu for interation

    # with open('inventory.csv', newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         try:
    #             Product.create(product_name=row['product_name'],
    #                             product_quantity=row['product_quantity'],
    #                             product_price=row['product_price'],
    #                             date_updated=row['date_updated'])
    #         except IntegrityError:


            # print('NAME: ', row['product_name'])
            # print('QUANTITY: ', row['product_quantity'])
            # print('PRICE: ', row['product_price'])
            # print('UPDATED: ', row['date_updated'])
