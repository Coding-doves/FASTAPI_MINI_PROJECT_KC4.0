from fastapi import FastAPI, Query, Path, Body
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


# Basic Query Parameters
@app.get("/item/")
def item(name, category, price):
    """
    Description: 
                Create an endpoint that accepts multiple query parameters and returns them in a structured format.
    Query Parameters: 
                    name, category, price
    Returns: a JSON response with the query parameters in a dictionary format.
    """
    return {
        "name": name,
        "category": category,
        "price": price
    }


# Query Parameters with Default Values and Optional Fields
@app.get("/search/")
def search(query: Optional[str] = None, page: int = 1, size: int = 5):
    """
    Description: 
                Create an endpoint that uses query parameters with default values and optional fields.

    Endpoint: /search/
    Query Parameters: 
                    query, page, size
    Returns: a JSON response with the search results and pagination info.
    """
    # Test data
    data = [
        {"id": 1, "name": "Cat school"},
        {"id": 2, "name": "Drama target"},
        {"id": 3, "name": "Kodecamp 4"},
        {"id": 4, "name": "Palatable store"},
        {"id": 5, "name": "Movers part 5"},
    ]

    # Filter the data based on the query
    if query:
        data = [i for i in data if query.lower() in i["name"].lower()]

    # Pagination
    start = (page - 1) * size
    end = start + size
    result = data[start:end]
    total = len(data)

    return {
        "results": result,
        "page": page,
        "size": size,
        "total": total
    }


class Address(BaseModel):
    street: str
    city: str
    zip:int


class Profile(BaseModel):
    bio: Optional[str] = None
    handle: Optional[str] = None


class User(BaseModel):
    name: str 
    email: str
    address: Address
    profile: Optional[Profile] = None


# Request Body with Nested Pydantic Models
@app.post("/users/")
def create_user(user:User):
    """
    Description: 
                Create an endpoint that accepts a complex JSON request body with nested Pydantic models.

    Endpoint: 
            /users/
    Request Body:
                Pydantic model with nested fields for address and profile
                User: name, email, address: Address
                Address: street, city, zip
                Profile: bio, handle
    Returns: the received data as JSON.
    """
    return user


# Query Parameters with String Validations
@app.post("/validate/")
def str_validation(username: str = Query(
                            ..., # parameter is required
                            min_length=3, # Minimum length for username
                            max_length=20, # Maximum length
                            regex="^[a-zA-Z0-9]+$" # Allowed: num, alpha, underscores
                    )):    
    """
    Description: 
                Create an endpoint that validates query parameters using string validations that includes length and regex.

    Endpoint: 
            /validate/
    Query Parameters: 
                    username
    Return a JSON response confirming the validation.
    """
    return {"User": username, "msg": "Validated"}


class Report(BaseModel):
    title: str
    content: str


# Combined Parameters and Validations
@app.post("/report/{report_id}")
def self_reporting(report_id: int = Path(..., gt=0), 
                    start_date: str = Query(None),
                    end_date: str = Query(None), 
                    report: Report = Body(...)):
    """
    Description: 
                Create an endpoint that combines path parameters, query parameters, and request body with validations.

    Endpoint: 
            /reports/{report_id}
    Path Parameter: report_id (must be positive)
    Query Parameters: start_date, end_date
    Request Body: Pydantic model with fields: title, content
    Returns: a JSON response summarizing all the received data.
    """
    return {
        "report_id": report_id,
        "start_date": start_date,
        "end_date": end_date,
        "title": report.title,
        "content": report.content
    }
