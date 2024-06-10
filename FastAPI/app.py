import shutil
from fastapi import FastAPI, File, HTTPException, Query, status, responses, Form, UploadFile
from typing import Optional, List, Annotated, Dict
from pydantic import BaseModel, Field, EmailStr, ValidationError
import bcrypt
import random
import string

app = FastAPI()


"""
TASK 1:
    Simple Blog Post Creation
Test:
    http://127.0.0.1:8000/blog/

    {
        "title": "Monthly Report",
        "content": "This is the content of the monthly report."
    }

    {
        "title": "My First Blog Post",
        "content": "This a journey through kodecamp 4.0, first blog post.",
        "author": "Brown Dove"
    }
    {
        "content": "This a journey through kodecamp 4.0, first blog post.",
        "author": "Brown Dove"
    }

"""
class CreateBlogPost(BaseModel):
    title:str = Field(...)
    content:str = Field(...)
    author: Optional[str] = Field(None)


class ResponseModelPost(BaseModel):
    id: int
    title:str
    content:str
    author: Optional[str]


blog_posts_saved: List[ResponseModelPost] = []
post_id = 1

@app.post("/blog/",
          response_model=ResponseModelPost,
          status_code=status.HTTP_201_CREATED)
def blog_post(post: CreateBlogPost):
    """
    Description: create a blog post 
    Parameter: post 
    Returns: status response and post
    """
    try:
        global post_id

        new_post = ResponseModelPost(
            id=post_id,
            title=post.title,
            content=post.content,
            author=post.author
        )


        blog_posts_saved.append(new_post)
        post_id += 1

        return new_post
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



"""
TASK 2:
    User Profile Update with Image Upload
Test:
    http://127.0.0.1:8000/update_profile/
    name	Brown Dove
    email	brown@example.com
    picture	[Upload Image]
"""
class ResponseModelUpdate(BaseModel):
    name: str
    email: str
    picture_url: Optional[str]

@app.post("/update_profile/", response_model=ResponseModelUpdate, status_code=status.HTTP_200_OK)
def update_profile(name: Annotated[str, Form(min_length=2, max_length=100)],
                   email: Annotated[EmailStr, Form()],
                   picture: Optional[UploadFile] = File(None)):
    """
    Endpoint: /update_profile/
    Query Parameters: name, emails, picture
    Returns: updated profile
    """
    try:
        dp = None

        # Save the uploaded image file and validate format
        if picture:
            if picture.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image format. Only JPG, JPEG and PNG are allowed.")

            file_location = f"images/{picture.filename}"
            with open(file_location, "wb") as file:
                shutil.copyfileobj(picture.file, file)

            dp = f"/{file_location}"

        details = ResponseModelUpdate(name=name, email=email, picture_url=dp)

        return details
     
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


"""
TASK 3:
    Product Search with Pagination and Filtering

Test: 
    Basic Search:
    http://localhost:8000/search/?q=laptop
    http://localhost:8000/search/?category=Electronics
    http://localhost:8000/search/?min_price=500
    http://localhost:8000/search/?max_price=200
    http://localhost:8000/search/?min_price=150&max_price=500

    Search with Pagination:
    http://localhost:8000/search/?page=1&page_size=5

    Combined Search:
    http://localhost:8000/search/?q=table&category=Furniture&min_price=100&max_price=200&page=1&page_size=4

"""
class ProductSearch(BaseModel):
    id: int
    name: str
    category: str
    price: float

class Pagination(BaseModel):
    page_number: Optional[int]
    page_size: Optional[int]

class ResponseModelProductSearch(BaseModel):
    total_filtered_product: int
    product: List[ProductSearch]
    paginate: Optional[Pagination]

# Sample products
products = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 999.99},
    {"id": 2, "name": "Smartphone", "category": "Electronics", "price": 499.99},
    {"id": 3, "name": "Desk Chair", "category": "Furniture", "price": 199.99},
    {"id": 4, "name": "Coffee Table", "category": "Furniture", "price": 149.99},
    {"id": 5, "name": "Coffee", "category": "Beverage", "price": 14.09},
    {"id": 6, "name": "Solfa Set", "category": "Furniture", "price": 109.99},
    {"id": 7, "name": "Bamboo Phone Stand", "category": "Deco", "price": 10.99},
]

@app.get("/search/", response_model=ResponseModelProductSearch, status_code=status.HTTP_200_OK)
def search_product(search_term: Optional[str] = Query(None, alias="q", min_length=1, max_length=100, strip_whitespace=True),
                   category: Optional[str] = None,
                   min_price: Optional[float] = None,
                   max_price: Optional[float] = None,
                   page: int = Query(1, ge=1),
                   page_size: int = Query(10, ge=1, le=100)):
    """
    Endpoint: /search/
    Query Parameters: search_term, category, min_price, max_price, page, page_size
    Returns: filtered and paginated list of products
    """
    try:
        filtered = products

        # Filter by search term
        if search_term:
            filtered = [product for product in filtered if search_term.lower() in product["name"].lower()]
        # Filter by category
        if category:    
            filtered = [product for product in filtered if product["category"].lower() == category.lower()]
        # Filter by min_price
        if min_price is not None:    
            filtered = [product for product in filtered if product["price"] >= min_price]
        # Filter by max_price
        if max_price is not None:    
            filtered = [product for product in filtered if product["price"] <= max_price]

        total_filtered_product = len(filtered)
        start_page = (page - 1) * page_size
        end = start_page + page_size
        filtered_product = filtered[start_page:end]

        paginate = Pagination(page_number=page, page_size=page_size)
        response = ResponseModelProductSearch(total_filtered_product=total_filtered_product, product=filtered_product, paginate=paginate)

        return response

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


"""
TASK 4:
    Secure Registration with OTP Verification
Test: 
    http://localhost:8000/register/
    email: user@example.com
    password: strongpassword
    phone_number: (optional)

    http://localhost:8000/verify_otp/
    {
        "phone_number":"07051481343",
        "otp":"check the Terminal"
    }
    {
        "email":"brown@example.com",
        "otp":"check the Terminal"
    }
"""
# In-memory data storage
users_db: Dict[str, 'User'] = {}
otp_db: Dict[str, str] = {}

def send_otp(destination: str, otp: str):
    # Send OTP to email or phone
    print(f"\nSending OTP {otp} to {destination}\n")


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


class User(BaseModel):
    email: EmailStr
    password_hash: str
    phone_number: Optional[str] = None
    is_verified: bool = False


class ResponseUserRegistration(BaseModel):
    user_id: str
    message: str


@app.post("/register_user/", response_model=ResponseUserRegistration, status_code=status.HTTP_201_CREATED)
def str_validation(email: EmailStr = Form(...),
                   password: str = Form(...),
                   phone_number: Optional[str] = Form(None)):    
    """
    Endpoint: /register_user/
    Query Parameters: email, password, phone_number
    Returns: user_id and msg
    """
    if email in users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    users_db[email] = User(email=email, password_hash=password_hash, phone_number=phone_number)

    otp = generate_otp()

    if phone_number:
        otp_db[phone_number] = otp
    else:
        otp_db[email] = otp

    send_otp(email if phone_number is None else phone_number, otp)

    return ResponseUserRegistration(user_id=user_id, message="Please verify the OTP sent to your email or phone")


class OTPVerificationResponse(BaseModel):
    message: str



@app.post("/verify_otp/", response_model=OTPVerificationResponse, status_code=status.HTTP_200_OK)
def verify_otp(email: Optional[EmailStr] = Form(None), phone_number: Optional[str] = Form(None), otp: str = Form(...)):
    """
    Endpoint: /verify_otp/
    Form Data: email, phone_number, otp
    Returns: success message if OTP is valid
    """
    print(otp)

    if not email and not phone_number:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or phone number must be provided")
    
    identifier = email if email else phone_number

    if identifier not in otp_db or otp_db[identifier] != otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")

    user = users_db[email] if email else next((user for user in users_db.values() if user.phone_number == phone_number), None)
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    user.is_verified = True

    del otp_db[identifier]

    return OTPVerificationResponse(message="User verified successfully")


"""
TASK 5:
    E-commerce Shopping Cart Management
Test:
    
"""
class CartItem(BaseModel):
    product_id: int
    quantity: int


class CartResponse(BaseModel):
    msg: str
    cart: Dict[int, CartItem]

@app.post("/cart/", response_model=CartResponse, status_code=status.HTTP_200_OK)
def shopping_cart():
    """
    Endpoint: 
    Returns: 
    """
    return {
        
    }
