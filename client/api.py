from tkinter import E
import requests
import json
import os


class BiblioAPI:
    def __init__(self, url: str = "http://localhost:8000") -> None:
        self.base = url.removesuffix("/")
        self.auth_data = None
        self.token = ""

    def status(self) -> bool:
        try:
            code = requests.get(self.base).status_code
            if code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

    def register_user(self, data: dict) -> bool:
        code = requests.post(f"{self.base}/registration", json.dumps(data)).status_code
        return code == 200

    def authenticate(self, data: dict) -> bool:
        t = os.popen(
            f'curl -X "POST" "{self.base}/token" -N -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=&username={data["username"]}&password={data["password"]}"'
        ).read()

        t = str(t)
        t = eval(t)
        self.token = t["access_token"]
        a = requests.get(f"http://localhost:8000/verification?token={self.token}")
        return a.status_code == 200

    def delete_product(self, product_id: str) -> bool:
        a = os.popen(
            f"curl -X 'DELETE' \
        '{self.base}/products/1' \
        -H 'accept: application/json' \
        -H 'Authorization: Bearer {self.token}'"
        ).read()
        a = eval(str(a))
        return a == {"status": "success"}

    def update_product(self, product_id: str, updated_data: dict) -> bool:
        """
        Schema for updated_data:
        {
        "name": proname,
        "genre": procat,
        "price": proprice,
        "cover_image": proimage,
        "date_published": prodate,
        "quantity": proqty
        }
        """
        a = os.popen(
            f"curl -X 'PATCH' \
        '{self.base}/products/{product_id}' \
        -H 'accept: application/json' \
        -H 'Authorization: Bearer {self.token}' \
        -H 'Content-Type: application/json' \
        -d '{json.dumps(updated_data)}'"
        ).read()
        a = eval(str(a))
        return a["status"] == "success"

    def get_product(self, product_id: str) -> dict:
        res = requests.get(f"{self.base}/products/{product_id}")
        data = res.json()
        return res.status_code == 200

    def create_product(self, product_data: dict) -> bool:
        """
        Schema for product_data:
        {
        "name": proname,
        "genre": procat,
        "price": proprice,
        "cover_image": proimage,
        "date_published": prodate,
        "quantity": proqty
        }
        """
        a = os.popen(
            f"curl -X 'POST' \
        '{self.base}/products' \
        -H 'accept: application/json' \
        -H 'Authorization: Bearer {self.token}' \
        -H 'Content-Type: application/json' \
        -d '{product_data}'"
        ).read()
        a = eval(str(a))
        return a["status"] == "success"

    def get_products_from_category(self, category: str) -> list:
        res = requests.get(f"{self.base}/filter/{category}")
        if res.status_code == 200:
            return res.json()
        else:
            return None
