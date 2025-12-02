# main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator  # Use @validator for Pydantic 1.x
from fastapi.exceptions import RequestValidationError
from app.operations import add, subtract, multiply, divide  # Ensure correct import path
from app.db import init_db, SessionLocal
from app.operations import users as user_ops
from app.operations import calculations as calc_ops
from app import schemas
from app.security import create_access_token
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Setup templates directory
templates = Jinja2Templates(directory="templates")

# Pydantic model for request data
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator('a', 'b')  # Correct decorator for Pydantic 1.x
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError('Both a and b must be numbers.')
        return value

# Pydantic model for successful response
class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")

# Pydantic model for error response
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")

# Custom Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extracting error messages
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(
        status_code=400,
        content={"error": error_messages},
    )

@app.get("/")
async def read_root(request: Request):
    """
    Serve the index.html template.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def add_route(operation: OperationRequest):
    """
    Add two numbers.
    """
    try:
        result = add(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Add Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/subtract", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def subtract_route(operation: OperationRequest):
    """
    Subtract two numbers.
    """
    try:
        result = subtract(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Subtract Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/multiply", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def multiply_route(operation: OperationRequest):
    """
    Multiply two numbers.
    """
    try:
        result = multiply(operation.a, operation.b)
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Multiply Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/divide", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def divide_route(operation: OperationRequest):
    """
    Divide two numbers.
    """
    try:
        result = divide(operation.a, operation.b)
        return OperationResponse(result=result)
    except ValueError as e:
        logger.error(f"Divide Operation Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Divide Operation Internal Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    # Initialize DB tables for local runs
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=8000)


# ========== User Endpoints ==========

@app.post("/users/register", response_model=schemas.Token)
def register_user(user_in: schemas.UserCreate):
    """Register a new user. Returns a JWT access token."""
    db = SessionLocal()
    try:
        user = user_ops.create_user(db, user_in)
        # Create JWT token with user information
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id, "email": user.email}
        )
        return schemas.Token(access_token=access_token, token_type="bearer")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@app.post("/users/login", response_model=schemas.Token)
def login_user(user_login: schemas.UserLogin):
    """Login a user by verifying username and password. Returns a JWT access token."""
    db = SessionLocal()
    try:
        user = user_ops.authenticate_user(db, user_login.username, user_login.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        # Create JWT token with user information
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id, "email": user.email}
        )
        return schemas.Token(access_token=access_token, token_type="bearer")
    finally:
        db.close()


# ========== Calculation Endpoints (BREAD) ==========

@app.post("/calculations", response_model=schemas.CalculationRead)
def create_calculation(calc_in: schemas.CalculationCreate):
    """Add a new calculation."""
    db = SessionLocal()
    try:
        calc = calc_ops.create_calculation(db, calc_in, store_result=True)
        return calc
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@app.get("/calculations", response_model=list[schemas.CalculationRead])
def browse_calculations(skip: int = 0, limit: int = 100):
    """Browse all calculations with pagination."""
    db = SessionLocal()
    try:
        calcs = calc_ops.get_all_calculations(db, skip=skip, limit=limit)
        return calcs
    finally:
        db.close()


@app.get("/calculations/{calc_id}", response_model=schemas.CalculationRead)
def read_calculation(calc_id: int):
    """Read a specific calculation by ID."""
    db = SessionLocal()
    try:
        calc = calc_ops.get_calculation_by_id(db, calc_id)
        if not calc:
            raise HTTPException(status_code=404, detail="Calculation not found")
        return calc
    finally:
        db.close()


@app.put("/calculations/{calc_id}", response_model=schemas.CalculationRead)
def update_calculation(calc_id: int, calc_in: schemas.CalculationCreate):
    """Edit an existing calculation."""
    db = SessionLocal()
    try:
        calc = calc_ops.update_calculation(db, calc_id, calc_in)
        if not calc:
            raise HTTPException(status_code=404, detail="Calculation not found")
        return calc
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@app.delete("/calculations/{calc_id}")
def delete_calculation(calc_id: int):
    """Delete a calculation by ID."""
    db = SessionLocal()
    try:
        deleted = calc_ops.delete_calculation(db, calc_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Calculation not found")
        return {"message": "Calculation deleted successfully"}
    finally:
        db.close()
