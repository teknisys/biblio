# from fastapi.testclient import TestClient

# from main import app

# client = TestClient(app)
from http import server
import requests
import json

api = "http://localhost:8000/"
reg = "registration/"
pro = "product/"
proid = "/"
fil = "filer/"
tok = "token/"
ver = "verification/"
add = "uploadfile/product/"
username = "Placeholder"
email = "yaba.doo@email.con"
password = "No"
proname = "FortniteBattlePass"
procat = "Gaming"
proprice = 1000
proimage = "battlepass.jpg"
prodate = "2022-08-06"
proqty = 100
file = "megaman.jpg"


def servercheck():
    ello = requests.get(api)
    if ello == 200:
        return True
    else:
        return False


def reg():
    data = {"username": username, "email": email, "password": password}
    register = requests.post(f"{api}{reg}", json.dumps(data))
    if register == 200:
        return True
    else:
        return False


def propost():
    data = {
        "name": proname,
        "genre": procat,
        "price": proprice,
        "cover_image": proimage,
        "date_published": prodate,
        "quantity": proqty,
    }
    product = requests.post(f"{api}{pro}", json.dumps(data))
    if product == 201:
        return True
    else:
        return False


def proget():
    product = requests.get(f"{api}{pro}")
    if product == 200:
        return True
    else:
        return False


def specpro():
    product = requests.get(f"{api}{pro}{proid}")
    print(product)
    if (
        product.body
        == {
            "name": "1984",
            "genre": "fiction",
            "price": 20,
            "quantity": 10,
            "business_id": 1,
        }
        and product.status == 200
    ):
        return True
    else:
        return False


def delpro():
    product = requests.delete(f"{api}{pro}{proid}")
    if product == 200:
        return True
    else:
        return False


def patchpro():
    data = {
        "name": proname,
        "genre": procat,
        "price": proprice,
        "cover_image": proimage,
        "date_published": prodate,
        "quantity": proqty,
    }
    product = requests.patch(f"{api}{pro}{proid}", json.dumps(data))
    if product == 200:
        return True
    else:
        return False


def filter():
    filter = requests.get(f"{api}{fil}{procat}/")
    if filter == 200:
        return True
    else:
        return False


def verify():
    data = {"username": username, "password": password}
    token = requests.post(f"{api}{tok}", json.dumps(data))
    verify = requests.get(f"{api}{ver}", token)
    if verify == 200:
        return True
    else:
        return False


def addfile():
    data = {file}
    addfile = requests.post(f"{api}{add}{proid}/", json.dumps(data))
    if addfile == 201:
        return True
    else:
        return False


# print(servercheck(), reg(), propost(), proget(), delpro(), patchpro(), filter(), addfile())
print(servercheck())
