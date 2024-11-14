from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, Request
from tortoise.contrib.fastapi import register_tortoise
from models import (
    User,
    Business,
    Product,
    user_pydantic,
    user_pydanticIn,
    product_pydantic,
    product_pydanticIn,
    business_pydantic,
    product_pydanticOut,
)

# signals
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient

from starlette.requests import Request

# authentication and authorization
import jwt
from dotenv import dotenv_values
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# self packages
from emails import *
from authentication import *
from dotenv import dotenv_values

from fastapi import File, UploadFile
import secrets

from fastapi.staticfiles import StaticFiles

from PIL import Image

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

config_credentials = dict(dotenv_values(".env"))

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
@limiter.limit("10/minute")
def api_check(request: Request):
    return {"status": "success", "data": "API is up and running!"}


oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# password helper functions
@app.post("/token")
@limiter.limit("10/minute")
async def generate_token(request: Request, request_form: OAuth2PasswordRequestForm = Depends()):
    token = await token_generator(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "bearer"}


# process signals
@post_save(User)
async def create_business(
    sender: "Type[User]",
    instance: User,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str],
) -> None:

    if created:
        business_obj = await Business.create(business_name=instance.username, owner=instance)
        await business_pydantic.from_tortoise_orm(business_obj)
        await send_email([instance.email], instance)


@app.post("/registration")
@limiter.limit("10/minute")
async def user_registration(user: user_pydanticIn, request: Request):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_password_hash(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)

    return {
        "status": "success",
        "data": {
            "message": f"Hi {new_user.username}, please check your email inbox and click on the link to confirm your registration."
        },
    }


# template for email verification
templates = Jinja2Templates(directory="templates")


@app.get("/verification", response_class=HTMLResponse)
@limiter.limit("10/minute")
async def email_verification(request: Request, token: str):
    user = await verify_token(token)
    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse("verification.html", {"request": request, "username": user.username})
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(request: Request, token: str = Depends(oath2_scheme)):
    try:
        payload = jwt.decode(token, config_credentials["SECRET"], algorithms=["HS256"])
        user = await User.get(id=payload.get("id"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await user


@app.post("/user/me")
@limiter.limit("10/minute")
async def user_login(request: Request, user: user_pydantic = Depends(get_current_user)):
    return {
        "status": "success",
        "data": {
            "username": user.username,
            "email": user.email,
            "verified": user.is_verified,
            "join_date": user.join_date.strftime("%b %d %Y"),
        },
    }


@app.post("/products", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def add_new_product(
    request: Request, product: product_pydanticIn, user: user_pydantic = Depends(get_current_user)
):
    # only email verified users can create products
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required",
        )

    product = product.dict(exclude_unset=True)

    product_obj = await Product.create(**product, business=user)
    product_obj = await product_pydantic.from_tortoise_orm(product_obj)
    return {"status": "success", "data": product_obj}


@app.get("/products")
@limiter.limit("10/minute")
async def get_products(request: Request):
    response = await product_pydanticIn.from_queryset(Product.all())
    return {"status": "success", "data": response}


@app.get("/products/{id}")
async def specific_product(id: int, request: Request):
    response = await product_pydantic.from_queryset_single(Product.get(id=id))
    return {
        "status": "success",
        "data": {
            "product_details": response,
        },
    }


@app.get("/filter/{genre}")
@limiter.limit("10/minute")
async def filter(genre: str, request: Request):
    response = await product_pydantic.from_queryset(Product.filter(genre=genre))
    if len(response) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No books found under genre {genre}")
    return {"status": "success", "data": response}


@app.delete("/products/{id}")
@limiter.limit("10/minute")
async def delete_product(id: int, request: Request, user: user_pydantic = Depends(get_current_user)):
    product = await Product.get(id=id)
    business = await product.business
    owner = await business.owner

    # only email verified users can delete
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required",
        )

    # check if the person requesting deletion is the business owner or superuser
    await product.delete()
    return {"status": "success"}


@app.patch("/products/{id}")
@limiter.limit("10/minute")
async def update_product(
    id: int, request: Request, product: product_pydanticIn, user: user_pydantic = Depends(get_current_user)
):
    # only email verified users can delete
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required",
        )
    await Product.filter(id=id).update(**product.dict(exclude_unset=True))
    res = await product_pydanticIn.from_queryset_single(Product.get(id=id))

    return {"status": "success", "data": res}


@app.post("/uploadfile/product/{id}", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_upload_file(
    id: int, request: Request, file: UploadFile = File(...), user: user_pydantic = Depends(get_current_user)
):
    product = await Product.get(id=id)
    business = await product.business
    owner = await business.owner

    FILEPATH = "./static/images/"
    filename = file.filename
    extension = filename.split(".")[1]

    if extension not in ["jpg", "png"]:
        return {"status": "error", "data": {"detail": "file extension not allowed"}}

    token_name = f"""{secrets.token_hex(10)}.{extension}"""
    generated_name = FILEPATH + token_name
    file_content = await file.read()
    with open(generated_name, "wb") as file:
        file.write(file_content)

    img = Image.open(generated_name)
    img = img.resize(size=(200, 200))
    img.save(generated_name)

    if owner == user:
        product.cover_image = token_name
        await product.save()

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated to perform this action",
            headers={"WWW-Authenticate": "Bearer"},
        )

    file_url = "localhost:8000" + generated_name[1:]
    return {"status": "success", "data": {"filename": file_url}}


@app.post("/checkout")
@limiter.limit("10/minute")
async def checkout(
    request: Request, orders: List[product_pydantic], user: user_pydantic = Depends(get_current_user)
):
    total_cost = 0
    for i in orders:
        i = dict(i)
        # not doing verification of request, placing my trust in the frontend
        product = await Product.get(id=i["id"])
        p = dict(product)

        if product.quantity < i["quantity"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Order quantity is greater than quantity in stock",
            )

        total_cost += p["price"] * i["quantity"]

        product.quantity -= i["quantity"]
        await product.save()

    return {"status": "success", "data": {"total_cost": total_cost}}


register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
