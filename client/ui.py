from rich import print
from rich.panel import Panel
from rich.prompt import Prompt,Confirm
from rich.console import Console
from rich.table import Table
from api import BiblioAPI
import json
import os
# console
c = Console()
api = BiblioAPI()
# Server Status Check
# online = api.status()
online  = True # use for testing
test_mode = False # test mode enabled

# Helpers
def saveCredentials(username,password):
        with open("creds.json","w") as f:
            json.dump({"username":username,"password":password},f)

def deleteCredentials():
    if(os.path.exists("creds.json")):
        os.remove("creds.json")

def loadSavedCredentials():
    if(os.path.exists("creds.json")):
        with open("creds.json","r") as f:
            data = json.load(f)
            return data
    else:
        return None

# Welcome to Biblio
def welcomeMessage():
    print(Panel.fit("The all in one bookstore for all your reading needs.", title="Welcome to Biblio", border_style="red",subtitle_align="center"))
    action = Prompt.ask("", choices=["Login", "Register"], default="Register")
    return action

# Register
def register():
    print(Panel.fit(title="Register", border_style="red"))
    username = Prompt.ask("Username")
    email = Prompt.ask("Email")
    password = Prompt.ask("Password", password=True)
    confirm = Confirm.ask("Confirm Signup")
    if confirm:
        return api.register_user({"username": username, "email": email, "password": password})
        
    else:
        exit(0)

# Login
def login():
    print(Panel.fit(title="Login", border_style="red"))
    saved = loadSavedCredentials()
    if saved is not None:
        return api.authenticate(saved)
    username = Prompt.ask("Username")
    password = Prompt.ask("Password", password=True)
    save = Confirm.ask("Save Credentials")
    if save:
        saveCredentials(username,password)
    else:
        deleteCredentials()
    return api.authenticate({"username": username, "password": password})

# Home
def home():
    c.clear()
    print(Panel.fit(title="Home", border_style="red"))
    action = Prompt.ask("", choices=["Search","Discover", "Exit"], default="Search")
    if(action == "Search"):
        displayResults(search())
    elif(action == "Discover"):
        displayResults(discover())
    else:
        exit(0)

def discover():
    return []
    c.clear()
    print(Panel.fit(title="Discover", border_style="red"))
    results = api.discover() #TODO: implement 
    return results

def search():
    c.clear()
    print(Panel.fit(title="Search", border_style="red"))
    category = Prompt.ask("Enter Category")
    results = api.get_products_from_category(category)
    return results

def createProduct():
    c.clear()
    print(Panel.fit(title="Add Product", border_style="red"))
    name = Prompt.ask("Name")
    price = Prompt.ask("Price")
    qty = Prompt.ask("Quantity")
    date = Prompt.ask("Date Published")
    genre = Prompt.ask("Genre")
    cov_image = Prompt.ask("Cover Image")
    return api.create_product({"name": name, "price": price, "qty": qty, "date": date, "genre": genre, "cov_image": cov_image})

def deleteProduct():
    c.clear()
    print(Panel.fit(title="Delete Product", border_style="red"))
    id = Prompt.ask("ID")
    confirm = Confirm.ask("Confirm Delete")
    if confirm:
        return api.delete_product(id)
    return None

def displayProductData(product_id: str = None):
    if product_id is None:
        product_id = Prompt.ask("Product ID")
    product = api.get_product(product_id)
    #TODO: create display layout
    return
    
def updateProduct(product_id: str = None):
    if product_id is None:
        product_id = Prompt.ask("Product ID")
    product = api.get_product(product_id)
    name = Prompt.ask("Name", default=product["name"])
    price = Prompt.ask("Price", default=product["price"])
    qty = Prompt.ask("Quantity", default=product["qty"])
    date = Prompt.ask("Date Published", default=product["date"])
    genre = Prompt.ask("Genre", default=product["genre"])
    cov_image = Prompt.ask("Cover Image", default=product["cov_image"])
    return api.update_product(product_id, {"name": name, "price": price, "qty": qty, "date": date, "genre": genre, "cov_image": cov_image})

def displayResults(results):
    table = Table(
        title="Results",
        show_header=True,
        header_style="bold magenta",
        show_lines=True,

    )
    table.add_column("ID", style="dim", width=12)
    table.add_column("Name", style="dim", width=20)
    table.add_column("Price", justify="right")
    table.add_column("Quantity", justify="right")
    table.add_column("Date Published", justify="right")
    table.add_column("Genre", justify="right")
    table.add_column("Cover Image", justify="right")
    i = 0
    for result in results:
        table.add_row(
            i,
            result["name"],
            str(result["price"]),
            str(result["qty"]),
            result["date"],
            result["genre"],
            result["cov_image"],
        )
        i+=1
    c.print(table)
    action = Prompt.ask("id")
    record = results[int(action)]
    displayRecord(record)
    
    #TODO: show results
    #TODO: show menu
def displayRecord(record):
    pass

# main program starts
if test_mode:
        if not online:
            print(Panel.fit("Please start server and try again.", title="Server Offline", border_style="red",subtitle_align="center"))
            exit(1)
        action = welcomeMessage()
        if action == "Register":
            register()
        else:
            login()
        while True:
            home()
else:
    pass #TODO: use this to test induvidual screens