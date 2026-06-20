from uuid import uuid4, UUID
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class Month(str,Enum):
    january = "january"
    february = "february"
    march = "march"
    april = "april"
    may = "may"
    june = "june"
    july = "july"
    august = "august"
    september = "september"
    october = "october"
    november = "november"
    december = "december"

class Token(BaseModel):
    access_token :str
    token_type :str
class TokenData(BaseModel):
    username: str |None = None
class User(BaseModel):
    username :str
    email: str | None = None
    full_name :str | None = None
    disabled : bool |None = None


class UserInDB(User):
    hashed_password :str
class TaskCreate(BaseModel):
    name : str
    category: Optional[str]
    description : Optional[str]
    month : Month
    completed: bool = False
class TaskEdit(BaseModel):
    name : str
    category: Optional[str]
    description : Optional[str]
    month : Month
    completed: bool = False
class Task(TaskCreate):
    id :int
    owner_username :str
    
class UserRegister(BaseModel):
    username :str
    email :str
    full_name :str
    password :str

