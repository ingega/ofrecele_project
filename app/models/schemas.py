from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str  # plain password
    email: str
    salt: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

class UserCreate(UserBase):
    pass