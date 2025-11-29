from fastapi import APIRouter
from pydantic import BaseModel, Field
from model import Teacher
from passlib.context import CryptContext

route = APIRouter()

Hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TeacherList(BaseModel):

    name: str = Field(min_length=3)
    email: str = Field(min_length=3)
    subject: str = Field(min_length=3)
    password: str


@route.post("/Create_teacher")
async def get_Teacher(CreateRqeuest: TeacherList):

    list = Teacher(
        name=CreateRqeuest.name,
        email=CreateRqeuest.email,
        subject=CreateRqeuest.subject,
        Hashpassword=Hashing.hash(CreateRqeuest.password),
    )

    return list
