from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from app.operations import add, subtract, multiply, divide
from typing import List, Optional


def compute_result(calc_in: schemas.CalculationCreate) -> float:
    t = calc_in.type
    if t == models.CalculationType.ADD:
        return add(calc_in.a, calc_in.b)
    if t == models.CalculationType.SUBTRACT:
        return subtract(calc_in.a, calc_in.b)
    if t == models.CalculationType.MULTIPLY:
        return multiply(calc_in.a, calc_in.b)
    if t == models.CalculationType.DIVIDE:
        return divide(calc_in.a, calc_in.b)
    raise ValueError("Unsupported calculation type")


def create_calculation(db: Session, calc_in: schemas.CalculationCreate, user_id: Optional[int] = None, store_result: bool = True) -> models.Calculation:
    result = None
    if store_result:
        result = compute_result(calc_in)

    calc = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
        user_id=user_id,
    )
    db.add(calc)
    try:
        db.commit()
        db.refresh(calc)
    except IntegrityError as e:
        db.rollback()
        raise
    return calc


def get_all_calculations(db: Session, user_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[models.Calculation]:
    """Browse all calculations with pagination. If user_id is provided, filter by user."""
    query = db.query(models.Calculation)
    if user_id is not None:
        query = query.filter(models.Calculation.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def get_calculation_by_id(db: Session, calc_id: int, user_id: Optional[int] = None) -> Optional[models.Calculation]:
    """Read a specific calculation by ID. If user_id is provided, verify ownership."""
    query = db.query(models.Calculation).filter(models.Calculation.id == calc_id)
    if user_id is not None:
        query = query.filter(models.Calculation.user_id == user_id)
    return query.first()


def update_calculation(db: Session, calc_id: int, calc_in: schemas.CalculationCreate, user_id: Optional[int] = None) -> Optional[models.Calculation]:
    """Edit an existing calculation. If user_id is provided, verify ownership."""
    calc = get_calculation_by_id(db, calc_id, user_id)
    if not calc:
        return None
    
    # Update fields
    calc.a = calc_in.a
    calc.b = calc_in.b
    calc.type = calc_in.type
    calc.result = compute_result(calc_in)
    
    try:
        db.commit()
        db.refresh(calc)
    except IntegrityError as e:
        db.rollback()
        raise
    return calc


def delete_calculation(db: Session, calc_id: int, user_id: Optional[int] = None) -> bool:
    """Delete a calculation by ID. Returns True if deleted, False if not found. If user_id is provided, verify ownership."""
    calc = get_calculation_by_id(db, calc_id, user_id)
    if not calc:
        return False
    
    db.delete(calc)
    db.commit()
    return True
