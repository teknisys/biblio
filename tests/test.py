import requests
import json
import os
import pytest

username = "badads"
email = "test@test.com"
password = "testing"
token = ""


def servercheck():
    ello = requests.get(f"http://localhost:8000/")
    return ello.status_code == 200


def register():
    data = {"username": username, "email": email, "password": password}
    regist = requests.post(f"http://localhost:8000/registration/", json.dumps(data))
    return regist.status_code == 200


def verify():
    global token
    token = os.popen(
        f'curl -X "POST" "http://127.0.0.1:8000/token" -N -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=&username={username}&password={password}"'
    ).read()
    token = str(token)
    token = eval(token)
    token = token["access_token"]
    a = requests.get(f"http://localhost:8000/verification?token={token}")
    return a.status_code == 200


def proget():
    product = requests.get("http://localhost:8000/products/")
    return product.status_code == 200


def filter():
    filter1 = requests.get(f"http://localhost:8000/filter/fiction/")
    filter2 = requests.get(f"http://localhost:8000/filter/Gaming/")
    return [filter1.status_code, filter2.status_code] == [200, 404]


def specpro():
    # autoPopulateDB.populateDB()
    product = requests.get("http://localhost:8000/products/1")
    p = eval(product.content)
    return (
        p["data"]["product_details"]["name"] == "1984"
        and p["data"]["product_details"]["price"] == 20
        and product.status_code == 200
    )


def test1():
    assert servercheck() == True


def test2():
    assert register() == True


def test3():
    assert verify() == True


def test4():
    assert filter() == True


def test4():
    assert proget() == True


def test4():
    assert specpro() == True
