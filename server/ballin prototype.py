import requests
import json
import tests.autoPopulateDB as autoPopulateDB

username = "ptolemy"
email = "bismillah@ixoti.com"
password = "SixCharacters123"
proname = "FortniteBattlePass"
procat = "Gaming"
proprice = 1000
proimage = "battlepass.jpg"
prodate = "2022-08-06"
proqty = 100


def servercheck():
    ello = requests.get(f"http://localhost:8000/")
    return ello.status_code == 200


def register():
    data = {"username": username, "email": email, "password": password}
    regist = requests.post(f"http://localhost:8000/registration/", json.dumps(data))
    if regist.status_code == 200:
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
    product = requests.post(f"http://localhost:8000/product/", json.dumps(data))
    if product.status_code == 201:
        return True
    else:
        return False


def proget():
    product = requests.get(f"http://localhost:8000/product/")
    if product.status_code == 200:
        return True
    else:
        return False


def specpro():
    # autoPopulateDB.populateDB()
    product = requests.get(f"http://localhost:8000/products/1")
    if (
        product.content
        == {
            "name": "1984",
            "genre": "fiction",
            "price": 20,
            "quantity": 10,
            "business_id": 1,
        }
        and product.status_code == 200
    ):
        return True
    else:
        return False


def delpro():
    product = requests.delete(f"http://localhost:8000/products/1")
    if product.status_code == 200:
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
    product = requests.patch(f"http://localhost:8000/products/1", json.dumps(data))
    if product.status_code == 200:
        return True
    else:
        return False


def filter():
    filter = requests.get(f"http://localhost:8000/filter/Gaming/")
    if filter.status_code == 200:
        return True
    else:
        return False


def verify():
    data = {"username": username, "password": password}
    token = requests.post(f"http://localhost:8000/token/", json.dumps(data))
    token = token.content
    print(token)
    a = requests.get(f"http://localhost:8000/verification/", token)
    if a.status_code == 200:
        return True
    else:
        return False


def addfile():
    file = open("static\images\d05391068b1f3cb2d72f.png", "rb")
    files = {"file": (file.name, file, "multi[art/form.data")}
    addfile = requests.post(url="http://localhost:8000/product/1", files=files)
    if addfile.status_code == 201:
        return True
    else:
        return False


print(servercheck())
print(register())
print(verify())
print(propost())
print(proget())
print(specpro())
print(delpro())
print(patchpro())
print(filter())
print(addfile())
