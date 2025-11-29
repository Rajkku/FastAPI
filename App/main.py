from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field
import model
from model import Table, Teacher
from database import engine, session
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from Router import route

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model.Base.metadata.create_all(bind=engine)

app.include_router(route.route)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


db_depend = Annotated[Session, Depends(get_db)]


class StudentList(BaseModel):

    name: str = Field(min_length=3)
    email: str = Field(min_length=3)

    phone_number: int

    address: str = Field(max_length=250)


@app.get("/getall/Student")
async def read_all(db: db_depend):
    return db.query(Table).all()


@app.get("/getby_id", status_code=status.HTTP_200_OK)
async def readby_id(db: db_depend, getid: int = Path(gt=0)):
    list = db.query(Table).filter(Table.id == getid).first()
    if list is not None:
        return list
    raise HTTPException(status_code=404, detail="Id is not fount")


@app.post("/Create/Student/List", status_code=status.HTTP_201_CREATED)
async def Create_student_list(db: db_depend, createRequest: StudentList):
    list = Table(**createRequest.model_dump())
    db.add(list)
    db.commit()


@app.put("/Update/Student/List/{reqID}", status_code=status.HTTP_201_CREATED)
async def Update_Student_list(
    db: db_depend, updateRequest: StudentList, reqID: int = Path(gt=0)
):
    list = db.query(Table).filter(Table.id == reqID).first()
    if list is None:
        raise HTTPException(status_code=404, detail="Item not found")
    list.name = updateRequest.name
    list.email = updateRequest.email
    list.phone_number = updateRequest.phone_number
    list.address = updateRequest.address

    db.add(list)
    db.commit()


@app.delete("/Delete{ReqID}")
async def Delete_list(db: db_depend, ReqID: int = Path(gt=0)):

    List = db.query(Table).filter(Table.id == ReqID).first()

    if List is None:
        raise HTTPException(status_code=404, detail="ID is not found")

    db.delete(List)
    db.commit()
    return {"Item deleted Succssefully"}
