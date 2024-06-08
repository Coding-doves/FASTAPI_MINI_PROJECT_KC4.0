import shutil
from fastapi import FastAPI, File, HTTPException, Query, Path, Body, status, responses, Form, UploadFile
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, EmailStr, ValidationError

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
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


"""
TASK 3:
    Product Search with Pagination and Filtering

Test: 
    
"""
class ProductSearch(BaseModel):
    id: int
    search_term: str
    category: str
    price_range: float

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
        # Filter by search term
        if search_term:
            filtered = [product for product in filtered if search_term.lower() in product["name"].lower()]
        # Filter by category
        if category:    
            filtered = [product for product in filtered if product["name"].lower() == category]
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
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


"""
TASK 4:
    Secure Registration with OTP Verification
Test: 
    
"""
@app.get("")
def str_validation():    
    """
    Description: 

    Endpoint: 
    Query Parameters: 
    Returns 
    """
    return {}


"""
TASK 5:
    E-commerce Shopping Cart Management
Test:
    
"""


# Combined Parameters and Validations
@app.post("/reports/{report_id}")
def self_reporting():
    """
    Description: 

    Endpoint: 
    
    Returns: 
    """
    return {
        
    }
