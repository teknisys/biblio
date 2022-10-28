from tkinter import E
import requests
import json
class BiblioAPI():
    def __init__(self,url: str = "http://localhost:8000") -> None:
        self.base = url.removesuffix('/')
        self.auth_data = None
    
    def status(self) -> bool:
        try:
            code = requests.get(self.base)
            if code == 200:
                return True
            else:
                return False
        except:
            return False

    def register_user(self,data: dict) -> bool:
        code = requests.post(self.base+"/registration", json.dumps(data))
        if code == 200:
            return True
        else:
            return False

    def authenticate(self,data: dict) -> bool:
        auth_data=requests.post(self.base+"/token", json.dumps(data))
        v_code=requests.get(self.base+"/verification", auth_data)
        if v_code == 200:
            self.auth_data = auth_data
            return True
        else:
            return False

    def delete_product(self,product_id: str) -> bool:
        code = requests.delete(self.base+f"/product/{product_id}")
        if code == 200:
            return True
        else:
            return False

    def update_product(self,product_id: str,updated_data: dict) -> bool:
        '''
        Schema for updated_data:
        {
        "name": proname,
        "genre": procat,
        "price": proprice,
        "cover_image": proimage,
        "date_published": prodate,
        "quantity": proqty
        }
        '''
        code = requests.patch(self.base+f'/product/{product_id}',json.dumps(updated_data))
        if code == 200:
            return True
        else:
            return False

    def get_product(self,product_id: str) -> dict:
        code = requests.get(self.base+f'/product/{product_id}')
        data = code.json()
        if code == 200:
            return data
        else:
            return None
    
    def create_product(self,product_data: dict) -> bool:

        '''
        Schema for product_data:
        {
        "name": proname,
        "genre": procat,
        "price": proprice,
        "cover_image": proimage,
        "date_published": prodate,
        "quantity": proqty
        }
        '''
        code = requests.post(self.base+'/product',json.dumps(product_data))
        if code == 201:
            return True
        else:
            return False

    def get_products_from_category(self,category: str) -> list:
        code = requests.get(self.base+f'/filter/{category}')
        if code == 200:
            return True
        else:
            return False
    
    def upload_file(self,file) -> bool:
        files = {
            "file": (file.name,file, "multipart/form.data")
        }
        code = requests.post(self.base+'/create_file',files=files)
        if code == 201:
            return True
        else:
            return False
    
 