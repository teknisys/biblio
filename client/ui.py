import time
from dateutil import parser
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.console import Console
from rich.table import Table
from api import BiblioAPI
import time
import json
import os

# console
c = Console()
api = BiblioAPI()
# Server Status Check
online = api.status()
online = True  # use for testing
test_mode = True  # test mode enabled

# Helpers
def saveCredentials(username, password):
    with open("creds.json", "w") as f:
        json.dump({"username": username, "password": password}, f)


def deleteCredentials():
    if os.path.exists("creds.json"):
        os.remove("creds.json")


def loadSavedCredentials():
    if os.path.exists("creds.json"):
        with open("creds.json", "r") as f:
            data = json.load(f)
            return data
    else:
        return None


# Welcome to Biblio
def welcomeMessage():
    print(
        Panel.fit(
            "The all in one bookstore for all your reading needs.",
            title="Welcome to Biblio",
            border_style="red",
            subtitle_align="center",
        )
    )
    action = Prompt.ask("", choices=["Login", "Register"], default="Login")
    return action


# Register
def register():
    c.clear()
    print(Panel.fit("Create an account", title="Register", border_style="red"))
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
    c.clear()
    print(Panel.fit("Access your existing account.", title="Login", border_style="red"))
    saved = loadSavedCredentials()
    if saved is not None:
        print("Found Saved Credentials")
        print("Logging In as " + f"[red]{saved['username']}[/red]")
        return api.authenticate(saved)
    username = Prompt.ask("Username")
    password = Prompt.ask("Password", password=True)
    save = Confirm.ask("Save Credentials")
    if save:
        saveCredentials(username, password)
    else:
        deleteCredentials()
    return api.authenticate({"username": username, "password": password})


def admin():
    c.clear()
    print(Panel.fit("Manage the products of biblio", title="Admin", border_style="red"))
    action = Prompt.ask("", choices=["Add", "Delete", "Display", "Update", "Exit"], default="Add")
    if action == "Add":
        success = createProduct()
        print("[green]Added Product Successfuly[/green]" if success else "[red]Failed to create[/red]")
        time.sleep(3)
    elif action == "Delete":
        success = deleteProduct()
        print("[green]Deleted Product Successfuly[/green]" if success else "[red]Failed to delete[/red]")
    elif action == "Display":
        success = displayProductData()
    elif action == "Update":
        success = updateProduct()
        print("[green]Updated Product Successfuly[/green]" if success else "[red]Failed to update[/red]")
    else:
        exit(0)


# Home
def home():
    c.clear()
    print(Panel.fit("Welcome to Biblio", title="Home", border_style="red"))
    action = Prompt.ask("", choices=["Search", "Admin", "Exit"], default="Search")
    if action == "Search":
        displayResults(search())
    elif action == "Admin":
        admin()
    else:
        exit(0)


def discover():
    c.clear()
    print(Panel.fit(title="Discover", border_style="red"))
    results = api.discover()  # TODO: implement
    if results == False:
        print("[red]Failed to retrieve content[/red]")
        time.sleep(3)
        return False
    return results


def search():
    c.clear()
    print(Panel.fit("Selected a Category", title="Search", border_style="red"))
    category = Prompt.ask("Enter Category") 
    results = api.get_products_from_category(category)

    return results


def createProduct():
    c.clear()
    print(Panel.fit("Add a new product", title="Add Product", border_style="red"))
    name = Prompt.ask("Name")
    price = Prompt.ask("Price")
    qty = Prompt.ask("Quantity")
    genre = Prompt.ask("Genre")
    return api.create_product(
        {
            "name": name,
            "price": price,
            "quantity": qty,
            "genre": genre,
        }
    )


def deleteProduct():
    c.clear()
    print(Panel.fit("Delete Product", border_style="red"))
    id = Prompt.ask("ID")
    confirm = Confirm.ask("Confirm Delete")
    if confirm:
        status = api.delete_product(id)
        print("[green]Deleted Product[/green]" if status else "[red]Failed to delete[/red]")
        time.sleep(3)
        return status
    return None


def displayProductData(product_id: str = None):
    if product_id is None:
        product_id = Prompt.ask("Product ID")
    product = api.get_product(product_id)
    # TODO: create display layout
    # print(product)
    if product is None:
        print("[red]Product Not Found[/red]")
        time.sleep(5)
        return False
    else:
        c.clear()
        displayRecord(product["data"]["product_details"])


def updateProduct(product_id: str = None):
    if product_id is None:
        product_id = Prompt.ask("Product ID")
    product = api.get_product(product_id)
    name = Prompt.ask("Name", default=product["data"]["product_details"]["name"])
    price = Prompt.ask("Price", default=product["data"]["product_details"]["price"])
    qty = Prompt.ask("Quantity", default=product["data"]["product_details"]["quantity"])
    genre = Prompt.ask("Genre", default=product["data"]["product_details"]["genre"])
    return api.update_product(
        product_id,
        {
            "name": name,
            "price": price,
            "quantity": qty,
            "genre": genre,
        },
    )


def displayResults(results):
    if results is None or len(results) == 0:
        print("[red]No Results Found[/red]")
        time.sleep(3)
        return False
    id_opts = []
    table = Table(
        title=f"{results['data'][0]['genre'].upper()} Genre",
        show_header=True,
        header_style="bold magenta",
        show_lines=True,
    )
    table.add_column("ID", style="dim bold", width=12)
    table.add_column("Name", style="dim bold", width=35)
    table.add_column("Price", justify="right")
    table.add_column("Quantity", justify="right")
    table.add_column("Date Published", justify="right")
    table.add_column("Genre", justify="right")
    # table.add_column("Cover Image", justify="right")
    i = 0
    for result in results["data"]:
        id_opts.append(str(result["id"]))
        table.add_row(
            str(result["id"]),
            result["name"],
            "INR {:.2f}".format(float(result["price"])),
            str(result["quantity"]),
            # parse a datetime string
            parser.parse(result["date_published"]).strftime("%Y-%m-%d"),
            result["genre"],
            # result["cover_image"],
        )
        i += 1
    c.print(table)
    action = Prompt.ask("Choose Product ID", choices=id_opts, default=id_opts[0])
    for result in results["data"]:
        if result["id"] == int(action):
            displayRecord(result)
            break


def displayRecord(record):
    l = Layout(name="root")
    metaL = Layout(name="meta", ratio=1)
    metaTable = Table(
        title=record["name"],
    )
    metaTable.add_column("")
    metaTable.add_column("")
    metaTable.add_row("ID", str(record["id"]))
    metaTable.add_row("Name", record["name"])
    # metaTable.add_row("Price", str(record["price"]))
    metaTable.add_row("Price", "INR {:.2f}".format(float(record["price"])))
    metaTable.add_row("Quantity", str(record["quantity"]))
    metaTable.add_row("Date Published", str(parser.parse(record["date_published"]).strftime("%Y-%m-%d")))
    metaTable.add_row("Genre", record["genre"])
    # pictL = Layout(name="image", ratio=1)
    l.split_column(metaL)
    metaL.update(metaTable)
    print(l)
    action = Prompt.ask("Choose Action", choices=["Buy Now", "back"], default="Buy Now")
    if action == "Buy Now":
        a = Prompt.ask(f"Enter quantity to buy")
        record["quantity"] = int(a)
        print("[red]Total cost:[/red]", record["quantity"] * int(a))
        confirm = Confirm.ask("Confirm Signup")
        if confirm:
            res = api.checkout([record])
            if not res:
                print("[red]Order quantity is greater than quantity in stock[/red]")
                time.sleep(2)
                displayRecord(record) 
            else:
                print("[green]Purchased Product Successfully![/green]")
                time.sleep(2)
        else:
            displayRecord(record) 
    else:
        return


# main program starts
if 1:
    c.clear()
    if not online:
        print(
            Panel.fit(
                "Please start server and try again.",
                title="Server Offline",
                border_style="red",
                subtitle_align="center",
            )
        )
        exit(1)
    action = welcomeMessage()
    if action == "Register":
        register()
    else:
        login()
    while True:
        home()

