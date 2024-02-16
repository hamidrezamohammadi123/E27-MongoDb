"""

Creating a system for a restaurant to manage its daily operations. 
This includes handling data for menus, orders, customer information, and customer feedback.

Database and Collection Setup:
1.	Create a MongoDB database named RestaurantDB.
2.	Set up the following collections: MenuItems, Orders, Customers, Customer Feedback.

Menu Management:
1.	Implement functionalities to add, view, update, and delete menu items.
2.	Each menu item should include name, price, category, and ingredients.

Order Management:
1.	Develop a system to handle customer orders, allowing for the creation, viewing, updating, and deletion of orders.
2.	Each order should be linked to menu items and customer id.

Customer Management:
1.	Create a system for managing customer data, including adding new customers, viewing customer details, and removing customer records.
2.	Each customer record should include an ID, name, phone number, and ....

Customer Feedback Management:
1.	Implement a feature to add and view customer feedback.

"""

from   pymongo import MongoClient
import uuid
import datetime
#import json

#---------------------------------- Connect to  database
client = MongoClient("mongodb://localhost:27017")

#---------------------------------- Set up the database a
db         = client["RestaurantDB"]
menu_items = db["MenuItems"]
orders     = db["Orders"]
customers  = db["Customers"]
customer_feedback = db["CustomerFeedback"]

#-------------------------------------------------------  MenuItem class
class MenuItem:
    def __init__(self, name, price, category, ingredients):
        self.name = name 
        self.price = price 
        self.category = category 
        self.ingredients = ingredients 

    def add_menu_item(self):
        menu_items.insert_one(self.__dict__) 
        print(f"Added {self.name} to the menu.")

    def view_menu_item(self, name):
        menu_item = menu_items.find_one({"name": name})
        print(menu_item) 

    def update_menu_item(self, name, new_name=None, new_price=None, new_category=None, new_ingredients=None):
        # Create a filter 
        filter = {"name": name}
        # Create with the new values
        update = {}
        if new_name:
            update["name"] = new_name
        if new_price:
            update["price"] = new_price
        if new_category:
            update["category"] = new_category
        if new_ingredients:
            update["ingredients"] = new_ingredients
        
        menu_items.update_one(filter, {"$set": update})
        print(f"Updated {name} in the menu.")

    def delete_menu_item(self, name):
        menu_items.delete_one({"name": name}) 
        print(f"Deleted {name} from the menu.")


#-----------------------------------------------------------------------

# Define the Order class
class Order:
    def __init__(self, customer_id, order_items):
        self.order_id = str(uuid.uuid4()) # Generate a unique id
        self.customer_id = customer_id 
        self.order_date = datetime.datetime.now() 
        self.order_status = "New" 
        self.order_items = order_items

    def add_order(self):
        orders.insert_one(self.__dict__) 
        print(f"Created a new order for customer {self.customer_id}.")

    def view_order(self, order_id):
        order = orders.find_one({"order_id": order_id}) 
        print(order)

    def update_order(self, order_id, new_status=None, new_menu_items=None):
        filter = {"order_id": order_id}
        update = {}
        if new_status:
            update["order_status"] = new_status
        if new_menu_items:
            update["order_items"] = new_menu_items
        
        orders.update_one(filter, {"$set": update})
        print(f"Updated order {order_id}.")

    def delete_order(self, order_id):
        orders.delete_one({"order_id": order_id}) 
        print(f"Deleted order {order_id}.")

#-----------------------------------------------------  Customer class

class Customer:
    def __init__(self, name, phone_number, email):
        self.customer_id = str(uuid.uuid4()) # Generate a unique id 
        self.name = name 
        self.phone_number = phone_number
        self.email = email 

    def add_customer(self):
        customers.insert_one(self.__dict__) 
        print(f"Added {self.name} as a new customer.")

    def view_customer(self, customer_id):
        customer = customers.find_one({"customer_id": customer_id}) 
        print(customer)

    def update_customer(self, customer_id, new_name=None, new_phone_number=None, new_email=None):
        filter = {"customer_id": customer_id}
        update = {}
        if new_name:
            update["name"] = new_name
        if new_phone_number:
            update["phone_number"] = new_phone_number
        if new_email:
            update["email"] = new_email
       
        customers.update_one(filter, {"$set": update})
        print(f"Updated customer {customer_id}.")

    def delete_customer(self, customer_id):
        customers.delete_one({"customer_id": customer_id}) 
        print(f"Deleted customer {customer_id}.")

#----------------------------------------------------- CustomerFeedback class

class CustomerFeedback:
    def __init__(self, customer_id, rating, comment):
        self.feedback_id = str(uuid.uuid4()) # Generate a unique id 
        self.customer_id = customer_id 
        self.feedback_date = datetime.datetime.now() 
        self.rating = rating 
        self.comment = comment

    def add_feedback(self):
        customer_feedback.insert_one(self.__dict__) 
        print(f"Added feedback from customer {self.customer_id}.")

    def view_feedback(self, feedback_id):
        feedback = customer_feedback.find_one({"feedback_id": feedback_id})
        print(feedback)

    def delete_feedback(self, feedback_id):
        customer_feedback.delete_one({"feedback_id": feedback_id}) 
        print(f"Deleted feedback {feedback_id}.")

#---------------------------------------  Main Body ---------------------------------------

def main():
    #  Some menu items
    abgosht = MenuItem("Ab Gosht", 200, "Main Course", ["Pea", "Beans", "Meat"])
    salad   = MenuItem("Salad"   , 50,  "Dessert",     ["Lettuce", "Carrot", "Dressing"])

                        # Add to the database
    abgosht.add_menu_item()
    salad.add_menu_item()

    #  Some customers
    ali = Customer("Ali",   "09123456789", "ali@gmail.com")
    sara = Customer("Sara", "02112345678", "sara@yahoo.com")

                        # Add to the database
    ali.add_customer()
    sara.add_customer()

    #  Some orders
    order1 = Order(ali.customer_id, [abgosht, salad])
    order2 = Order(sara.customer_id, [salad])

                         # Add to the database
    order1.add_order()
    order2.add_order()

    # Update  order status
    order1.update_order(order1.order_id, "Ready")
    order2.update_order(order2.order_id, "Delivered")

    #  Some feedback
    feedback1 = CustomerFeedback(ali.customer_id, 5, "Great service")
    feedback2 = CustomerFeedback(sara.customer_id, 3, "Bad food")

                         # Add  to the database
    feedback1.add_feedback()
    feedback2.add_feedback()


if __name__ == "__main__":
    # Call the main function
    main()



