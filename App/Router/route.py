from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel, Field
from model import Teacher
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError


route = APIRouter()

SCERECT_KEY = "4a25e8316eab083f2eb136d1d51eb78bc292a7ea1b7818dedfe6bd7d91374976"
ALGORITHM = "HS256"

Hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")

Bearer = OAuth2PasswordBearer(
    tokenUrl="token",
)


class TeacherList(BaseModel):

    name: str = Field(min_length=3)
    email: str = Field(min_length=3)
    subject: str = Field(min_length=3)
    password: str


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


db_depend = Annotated[Session, Depends(get_db)]


# logic for checking User authentication or not
def authenticate(username: str, password: str, db):
    list = db.query(Teacher).filter(Teacher.name == username).first()

    if not list:

        raise HTTPException(detail="No user found")
    if not Hashing.verify(password, list.Hashpassword):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No password found"
        )

    return list


def jws(username: str, user_id: int, Time: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + Time
    encode.update({"exp": expires})
    return jwt.encode(encode, SCERECT_KEY, algorithm=ALGORITHM)


async def getbeartoken(token: Annotated[str, Depends(OAuth2PasswordBearer)]):
    try:
        paylod = jwt.decode(token, SCERECT_KEY, algorithms=ALGORITHM)
        username: str = paylod.get("sub")
        userid: int = paylod.get("id")
        if username is None or userid is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return {"userName": username, "userid": userid}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@route.get("/get_All_Teacher")
async def get_all_teacher(db: db_depend):
    return db.query(Teacher).all()


@route.post("/Create_teacher", status_code=status.HTTP_200_OK)
async def get_Teacher(db: db_depend, CreateRqeuest: TeacherList):

    list = Teacher(
        name=CreateRqeuest.name,
        email=CreateRqeuest.email,
        subject=CreateRqeuest.subject,
        Hashpassword=Hashing.hash(CreateRqeuest.password),
    )
    db.add(list)
    db.commit()


@route.post("/getAuth")
def getAuth(data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_depend):

    user = authenticate(data.username, data.password, db)
    if not user:
        return {"Authenication failed"}
    token = jws(user.name, user.id, timedelta(minutes=20))
    return {"access-token": token, "token-type": "bearer"}
