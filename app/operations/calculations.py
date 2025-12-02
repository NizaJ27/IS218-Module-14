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


def create_calculation(db: Session, calc_in: schemas.CalculationCreate, store_result: bool = True) -> models.Calculation:
    result = None
    if store_result:
        result = compute_result(calc_in)

    calc = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
    )
    db.add(calc)
    try:
        db.commit()
        db.refresh(calc)
    except IntegrityError as e:
        db.rollback()
        raise
    return calc


def get_all_calculations(db: Session, skip: int = 0, limit: int = 100) -> List[models.Calculation]:
    """Browse all calculations with pagination."""
    return db.query(models.Calculation).offset(skip).limit(limit).all()


def get_calculation_by_id(db: Session, calc_id: int) -> Optional[models.Calculation]:
    """Read a specific calculation by ID."""
    return db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()


def update_calculation(db: Session, calc_id: int, calc_in: schemas.CalculationCreate) -> Optional[models.Calculation]:
    """Edit an existing calculation."""
    calc = get_calculation_by_id(db, calc_id)
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


def delete_calculation(db: Session, calc_id: int) -> bool:
    """Delete a calculation by ID. Returns True if deleted, False if not found."""
    calc = get_calculation_by_id(db, calc_id)
    if not calc:
        return False
    
    db.delete(calc)
    db.commit()
    return True
