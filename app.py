from collections import OrderedDict
import csv
import datetime
from datetime import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length =255, unique=True)
    product_quantity = IntegerField(default=0)
    product_price = IntegerField(default=0)
    date_updated = DateTimeField(default=datetime.now, formats = ['%m/%d/%Y'])

    class Meta:
        database = db


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Product], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

    
def transform_db():
    with open('inventory.csv', newline ='') as csvfile:
        file_reader = csv.DictReader(csvfile, delimiter = ',')
        my_inventory = list(file_reader)
        for item in my_inventory:
            item['product_price'] = float(item['product_price'].replace("$", "")) * 100
            item['product_price'] = int(item['product_price'])
            item['product_quantity'] = int(item['product_quantity'])
            item['date_updated'] =  datetime.strptime(item['date_updated'],'%m/%d/%Y').date()     
                
        csvfile.close()

    for item in my_inventory:
        try:
            Product.create(
                product_name = item['product_name'],
                product_price = item['product_price'],
                product_quantity = item['product_quantity'],
                date_updated = item['date_updated'])
        except IntegrityError: 
                product_record = Product.get(product_name=item['product_name'])
                product_record.price = item['product_price']
                product_record.quantity = item['product_quantity']
                product_record.date_updated = item['date_updated']
                product_record.save()

                
def view_product(search_id=None):
    try:
        view_p = Product.select().where(Product.product_id==search_id)
        if view_p:
            for item in view_p:
                print("*** ID: {} ***".format(item.product_id), "\n","Product: {}.".format(item.product_name),"\n", "Total amount in stock: {}".format(item.product_quantity),"\n","Current price: {}".format(item.product_price), "\n", "Last time updated: {}".format(item.date_updated)
                
                )
                
        else:
            print("Id not found. Try again.")
            search_product()

    except ValueError: 
        print("This is not a valid entry. Try again.")
        search_product()
         

def search_product():
    """View a product using the 'product_id'"""
    view_product(input('Search id: '))
    

def add_product():
    """Add a product to the inventory."""
    while True:
        
        new_product = input("Please enter your product name: ")

        try:
            entry_2 = float(input("Enter the price of the product: $")) *100
            integer_value = int(entry_2)
            new_p_quantity = int(input("Enter the quantity for the inventory: "))
            timestamp = datetime.now().date()
        except ValueError:
            print('This is not a valid entry. Try again using numbers only.')
            continue
        
        save_or_not = input('Save entry? [Yn] ').lower() 
        try:
            
                if save_or_not != 'n':
                    Product.create(
                        product_name = new_product,
                        product_price = integer_value,
                        product_quantity = new_p_quantity,
                        date_updated = timestamp
                                )
                    print(f"{new_product} saved successfully!".title())


        except IntegrityError:
            question = input("This product already exists. Would you like to update it? [Yn] ")
            if question == "y".lower().strip():
                Product.update(
                    product_price = entry_2,
                    product_quantity = new_p_quantity,
                    date_updated = timestamp).where(Product.product_name==new_product).execute()
                print("Product updated!","\n")
            elif question == "n".lower().strip():
                print("Thanks!")
                break

        continue_or_not = input("Type 'c' to continue adding products or 'r' to return to main menu: ").lower().strip()
        if continue_or_not == 'c':
            continue
        elif continue_or_not == 'r':
            break
            

def backup_db():
    """Backup the inventory database. """
    backup = 'the_latest_inventory.csv'
    fieldnames = ['product_id','product_name', 'product_price', 'product_quantity', 'date_updated']
    with open(backup, 'w', newline='') as csvfile:
        dbwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        dbwriter.writeheader()
        
        for item in Product.select().order_by(Product.product_id.desc()):
            dbwriter.writerow({
                'product_id': item.product_id,
                'product_name': item.product_name,
                'product_price': item.product_price,
                'product_quantity': item.product_quantity,
                'date_updated': item.date_updated})
        print("********************")
        print("Backup successful.")
        print("********************", "\n")

        csvfile.close() 

        menu()


my_menu = OrderedDict([
    ('a',add_product),
    ('b', backup_db),
    ('v', search_product),
])   


def menu():
    print("--------\n  MENU  \n--------")
    choice = None

    while choice != 'q':
        print("\nEnter 'q' to quit.\n")
        for key, value in my_menu.items():
            print('{}) {}'.format(key, value.__doc__))
            
        choice = input("Action:  ").lower().strip()
        clear()
        if choice not in my_menu:
            print("This is not a valid choice. Try again.")
            continue
        elif choice in my_menu:
            my_menu[choice]()
        

if __name__ == '__main__':
    initialize()
    transform_db()
    menu()
   