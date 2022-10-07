from rich import print
from rich.panel import Panel
from rich.prompt import Prompt,Confirm
from rich.console import Console
from api import BiblioAPI
# console
c = Console()
api = BiblioAPI()
# Server Status Check
online = api.status()
print(Panel.fit("Please start server and try again.", title="Server Offline", border_style="red",subtitle_align="center"))

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
    username = Prompt.ask("Username")
    password = Prompt.ask("Password", password=True)
    save = Confirm.ask("Remember Me")
    return api.authenticate({"username": username, "password": password})

# Home
def home():
    #TODO: Get List Of Products
    #TODO: EAdd Search bar
    pass

# main program starts
lor = welcomeMessage()
if lor == "Register":
    c.clear()
    register()
    c.clear()
else:
    c.clear()
    login()
    c.clear()


