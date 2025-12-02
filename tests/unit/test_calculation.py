import pytest
from pydantic import ValidationError

from app import schemas, operations, models
from app.operations import calculations as calc_ops


def test_compute_result_operations():
    c_add = schemas.CalculationCreate(a=2, b=3, type=models.CalculationType.ADD)
    assert calc_ops.compute_result(c_add) == 5

    c_sub = schemas.CalculationCreate(a=5, b=3, type=models.CalculationType.SUBTRACT)
    assert calc_ops.compute_result(c_sub) == 2

    c_mul = schemas.CalculationCreate(a=4, b=2.5, type=models.CalculationType.MULTIPLY)
    assert calc_ops.compute_result(c_mul) == 10.0

    c_div = schemas.CalculationCreate(a=9, b=3, type=models.CalculationType.DIVIDE)
    assert calc_ops.compute_result(c_div) == 3.0


def test_invalid_divisor_raises_validation_error():
    with pytest.raises(ValidationError):
        # b == 0 with Divide should raise on model creation
        schemas.CalculationCreate(a=1, b=0, type=models.CalculationType.DIVIDE)
