from typing import Optional

# from fastapi import FastAPI
from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class students:
    id: int
    name: str
    age: int
    mail: str
    pincode: int

    def __init__(self, id, name, age, mail, pincode,):
        self.id = id
        self.name = name
        self.age = age
        self.mail = mail
        self.pincode = pincode


class Create_studentlist(BaseModel):
    id: Optional[int] = Field(
        description="id is not required while create", default=None
    )
    name: str = Field(min_length=3)
    age: int = Field(gt=18, le=45)
    mail: str = Field(max_length=99, min_length=3)
    pincode: int = Field(ge=100000, le=999999)
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "enter the name",
                "age": 20,
                "mail": "Enter the email",
                "pincode": 1234,
            },
        }
    }


student = [
    students(1, "Raj", 15, "raj@gmail.com", 607002),
    students(2, "kumar", 17, "wq@gmail.com", 14597),
    students(3, "jayraj", 5, "lkj@gmail.com", 789654),
    students(4, "Gopal", 9, "vbn@gmail.com", 142563),
    students(5, "swaminathan", 8, "oplk@gmail.com", 741528),
]


@app.get("/get_studetnt/list", status_code= status.HTTP_200_OK)
def getall_students():
    return student


# @app.post("/create_student_list")

# def create_students(new_student=Body()):
#     student.append(new_student)
#     return student


@app.post("/Student/list/validation",status_code=status.HTTP_201_CREATED)
def create_list(list: Create_studentlist):
    newList = students(**list.model_dump())
    student.append(getid(newList))
    # return student


def getid(value: student):

    if len(student) > 0:
        value.id = student[-1].id + 1

    else:
        value.id = 1

    return value


@app.get("/filter_byage")
def filter_by_age(filter: int = Query(gt=18 ,le=45)):

    filter_list = []

    for i in student:
        if i.age == filter:
            filter_list.append(i)
        if filter_list:
            return filter_list
        raise HTTPException(status_code=404,detail="Item not found")
    return filter_list


@app.put("/update/student/list")
def update_list(update: Create_studentlist):

    for list in range(len(student)):

        if student[list].id == update.id:
            student[list] = update

# implemented for validation for path paramter
@app.delete("/delete_student{del_id}")
def delete_student(del_id:int = Path(gt=0)): 
    delete_status=False
    for i in range(len(student)):
        if student[i].id == del_id:
            delete_status=True
            student.pop(i)
            break
    if not delete_status:
        raise HTTPException(status_code=404,detail="Delete is already deleted")

# list = []
# for _ in range(int(input())):

#     n = input("Enter the name:")
#     m = float(input("Enter the marks"))

#     list.append([n, m])


# list.sort()
# scores = sorted({e for e, s in list})
# print(scores, "this is my sample list")
# print(scores[1])

# x = int(input())
# y = int(input())
# z = int(input())
# n = int(input())

# coordinates = [[i, j, k]
#                for i in range(x+1)
#                for j in range(y+1)
#                for k in range(z+1)
#                if i + j + k != n]

# print(coordinates)
