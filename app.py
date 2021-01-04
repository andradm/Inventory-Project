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

    
my_inventory = []

with open('inventory.csv', newline ='') as csvfile:
    file_reader = csv.DictReader(csvfile, delimiter = ',')
    
    for dictionary in file_reader:
        new_dict = {'product_id': Product().product_id}
        for key, value in dictionary.items():
            if key == "product_price":
                value = value.replace("$", "")
                int_value = int(float(value) * 100)
                new_dict[key] = int_value
            elif key == 'product_quantity':
                new_dict[key] = int(value)
            elif key == 'date_updated':
                new_dict[key] = datetime.strptime(
                    f'{value} 00:00:00', '%m/%d/%Y %H:%M:%S').date()
            else:
                new_dict[key] = value
    csvfile.close()
    my_inventory.append(new_dict)

       
def transform_db():
    for item in my_inventory:
        try:
            Product.create(
                product_id = item['product_id'],
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
    view_p = Product.select().where(Product.product_id==search_id)
    if view_p:
        for item in view_p:
            print("ID: {}".format(item.product_id))
            print("Product: {}.".format(item.product_name))
    else:
        print("Id not found. Try again.")
        search_product()
            

def search_product():
    """Display a product using the 'product_id'"""
    view_product(input('Search id: '))
    

            
def add_product():
    """Add a product to the inventory."""
    while True:
        
        new_product = input("Please enter your product name: ")

        try:
            entry_2 = float(input("Enter the price of the product: $"))
            clean_price = int(entry_2 * 100)
            new_p_quantity = int(input("Enter the quantity for the inventory: "))
            timestamp = datetime.now().date()
        except ValueError:
            print('This is not a valid entry. Try again using numbers only.')
            continue

        save_or_not = input('Save entry? [Yn] ').lower() 
        if save_or_not != 'n':
            Product.create(
                product_name = new_product,
                product_price = clean_price,
                product_quantity = new_p_quantity,
                date_updated = timestamp
                        )
            print(f"{new_product} saved successfully!".title())

        continue_or_not = input("Type 'c' to continue adding products, 'r' to return to main menu or 'q' to quit: ").lower().strip()
        if continue_or_not == 'c':
            continue
        elif continue_or_not == 'r':
            menu()
        elif continue_or_not == 'q':
            print("Thanks!")
            break
        

def backup_db():
    """Backup the inventory database. """
    backup = 'latest_inventory.csv'
    fieldnames = ['product_id','product_name', 'product_price', 'product_quantity', 'date_updated']
    with open(backup, 'w', newline='') as csvfile:
        dbwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        dbwriter.writeheader()
        
        for item in Product.select().order_by(Product.product_id.desc()):
            dbwriter.writerow({'product_id': item.product_id})
            dbwriter.writerow({'product_name': item.product_name})
            dbwriter.writerow({'product_price': item.product_price})
            dbwriter.writerow({'product_quantity': item.product_quantity})
            dbwriter.writerow({'date_updated': item.date_updated})

        print("Backup successful.")

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
        if choice in my_menu:
            my_menu[choice]()
        
                

if __name__ == '__main__':
    initialize()
    transform_db()
    menu()
   
    

  
    

                
    






            
   





