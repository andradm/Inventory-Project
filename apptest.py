from peewee import *

import csv
import datetime
from datetime import datetime


db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField(primary_key = True, unique=True)
    product_name = CharField(max_length =255, unique=True)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField(default=datetime.now, formats = ['%m/%d/%Y'])
    

    class Meta:
        database = db
my_inventory = []
with open('inventory.csv', newline ='') as csvfile:
    file_reader = csv.DictReader(csvfile, delimiter = ',')

    for dictionary in file_reader:
        for key, value in dictionary.items():
            if key == "product_price":
                value = value.replace("$", "")
                value = int(float(value) * 100)
            elif key == 'product_quantity':
                value = int(value)
            elif key == 'date_updated':
                value = datetime.strptime(
                    f'{value} 00:00:00', '%m/%d/%Y %H:%M:%S').date()
            else:
                 value = value
    
            my_inventory.append(dictionary)

print(my_inventory)

                 # try:
#         Product.create(
#             product_name = dictionary['product_name'],
#             product_price = dictionary['product_price'],
#             product_quantity = dictionary['product_quantity'],
#             date_updated = dictionary['date_updated'])



    

    
    

# if __name__ == '__main__':
#     db.connect()
#     db.create_tables([Product], safe=True)
    

                  
    






            
   





