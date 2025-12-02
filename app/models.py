from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint, Float, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum
from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        UniqueConstraint("email", name="uq_users_email"),
    )


# Calculation type enumeration
class CalculationType(str, Enum):
    ADD = "Add"
    SUBTRACT = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(SQLEnum(CalculationType, name="calculation_type"), nullable=False)
    result = Column(Float, nullable=True)
    # optional reference to users table if available
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", backref="calculations")
