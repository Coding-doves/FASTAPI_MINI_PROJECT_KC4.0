from fastapi import FastAPI, Depends, HTTPException
from typing import Callable
from datetime import datetime
from pydantic import BaseModel


app = FastAPI()

"""
TASK 1
"""
# arithmetic operators functions
def add(a:float, b:float) -> float:
    return a + b


def subtraction(a:float, b:float) -> float:
    return a - b


def multiplication(a:float, b:float) -> float:
    return a * b


def division(a:float, b:float) -> float:
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    return a / b


# Dependency injection function
def operation(operation: str) -> Callable[[float, float], float]:
    operators_func = {
        "add": add,
        "subract": subtraction,
        "multiply": multiplication,
        "divide": division
    }

    if operation not in operators_func:
        raise HTTPException(status_code=400, detail="Invalid operator")
    return operators_func[operation]


# Endpoint to perform the operation
@app.get("/calculate/{operator}")
def calculate(operator:str, num1:float, num2:float, func:Callable[[float, float], float] = Depends(operation)):
    result = func(num1,num2)
    return {"operator": operator, "num1": num1, "num2": num2, "result": result}


"""
TASK 2
"""
# Define the greeting messages based on the time of day
def morning_greeting() -> str:
    return "Good morning!"

def afternoon_greeting() -> str:
    return "Good afternoon!"

def evening_greeting() -> str:
    return "Good evening!"

def night_greeting() -> str:
    return "Good night!"

def greetings(hour: int = Depends(lambda: datetime.now().hour)) -> str:
    if 5 <= hour < 12:
        return morning_greeting()
    elif 12 <= hour < 18:
        return afternoon_greeting()
    elif 18 <= hour < 22:
        return evening_greeting()
    else:
        return night_greeting()

# Endpoint to get the greeting message
@app.get("/greet")
def greet(message: str = Depends(greetings)):
    return {"message": message}


"""
TASK 3
"""
# In-memory store for feature flags
FLAGS = {
    "dark_mode": False,
    "reset": False,
    "auto_bright": True
}

# Dependency to get the current state of a feature flag
def feature_flag(flag_name:str) -> bool:
    if flag_name not in FLAGS:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    return FLAGS[flag_name]

# Model for updating feature flags
class FeatureFlagUpdate(BaseModel):
    flag_name:str
    enable:bool

# Endpoint to get status of a feature flag
@app.get("/feature/{flag_name}")
def get_feature_status(flag_name:str, enabled:bool = Depends(feature_flag)):
    return {"feature": flag_name, "enabled": enabled}

# Endpoint to update the status of a feature flag
@app.put("/feature")
def update_feature_status(update: FeatureFlagUpdate):
    if update.flag_name not in FLAGS:
        raise HTTPException(status_code=404, detail="Feature not found")
    FLAGS[update.flag_name] = update.enabled
    return {"feature": update.flag_name, "enable": update.enabled}

# Example endpoint that is conditionally enabled based on a feature flag
@app.get("/example_one")
def example_one(enabled: bool = Depends(lambda: feature_flag("dark_mode"))):
    if not enabled:
        raise HTTPException(status_code=403, detail="Dark mode is disabled")
    return {"message": "Dark mode enabled"}

@app.get("/example_2")
def example_one(enabled: bool = Depends(lambda: feature_flag("auto_bright"))):
    if not enabled:
        raise HTTPException(status_code=403, detail="Auto bright is disabled")
    return {"message": "Auto bright enabled"}

@app.get("/example_3")
def example_one(enabled: bool = Depends(lambda: feature_flag("reset"))):
    if not enabled:
        raise HTTPException(status_code=403, detail="Reset is disabled")
    return {"message": "Reset activated"}


"""
TASK 4
"""
