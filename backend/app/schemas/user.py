from pydantic import BaseModel, Emailstr

class UserCreate(BaseModel):
    username: str
    email: Emailstr
    password: str

class userResponse(BaseModel):
    id: int
    username: str
    email: Emailstr
    

    class Config:
        from_attributes = True