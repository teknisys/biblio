from tortoise import models
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, null=False, unique=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    password = fields.CharField(max_length=100, null=False)
    is_verified = fields.BooleanField(default=False)
    join_date = fields.DatetimeField(default=datetime.utcnow)


class Business(models.Model):
    id = fields.IntField(pk=True, index=True)
    owner = fields.ForeignKeyField("models.User", related_name="business")


class Product(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=False, index=True)
    genre = fields.CharField(max_length=20, index=True)
    price = fields.DecimalField(max_digits=12, decimal_places=2)
    cover_image = fields.CharField(max_length=200, null=False, default="productDefault.jpg")
    date_published = fields.DatetimeField(default=datetime.utcnow)
    business = fields.ForeignKeyField("models.Business", related_name="products")
    quantity = fields.IntField()


user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified",))
user_pydanticIn = pydantic_model_creator(
    User, name="UserIn", exclude_readonly=True, exclude=("is_verified", "join_date")
)
user_pydanticOut = pydantic_model_creator(User, name="UserOut", exclude=("password"))

business_pydantic = pydantic_model_creator(Business, name="Business")
business_pydanticIn = pydantic_model_creator(Business, name="Business", exclude_readonly=True)


product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydanticIn = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)
product_pydanticOut = pydantic_model_creator(
    Product, name="ProductOut", exclude=("id", "genre", "price", "cover_image", "date_published", "business")
)
