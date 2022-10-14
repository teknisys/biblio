from rich import print
from rich.panel import Panel
from rich.prompt import Prompt,Confirm
from rich.console import Console
from api import BiblioAPI
import json
import os
# console
c = Console()
api = BiblioAPI()
# Server Status Check
# online = api.status()
online  = True # use for testing

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
    return
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

def displayResults(results):
    print(results)
    #TODO: show results
    #TODO: show menu

# main program starts
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
