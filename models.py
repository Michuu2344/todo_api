from uuid import uuid4, UUID
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

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
class Task(BaseModel):
    id : Optional[UUID] = Field(default_factory = uuid4())
    name : str
    category: Optional[str]
    description : Optional[str]
    month : Month
    


