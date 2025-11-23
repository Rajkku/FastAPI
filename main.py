from fastapi import FastAPI,Body

app=FastAPI()

students = [
    {"name": "Raj kumar", "age": 20, "course": "Python"},
    { "name": "Kiran", "age": 21, "course": "Java"},
    { "name": "Meena", "age": 19, "course": "Data Science"},
    { "name": "Arun", "age": 22, "course": "Python"},
    { "name": "kumar", "age": 22, "course": "Python"},
    { "name": "jhon", "age": 22, "course": "Python"},
]

# print(students)

#  get method
@app.get('/student')
def Get_students():
    return students


# path parameter
@app.get('/student/{param}')

def get_course(param:str):
    for s in students:
        if s.get('name').casefold() == param.casefold():
            return s
        
# Query parametr 
# 
@app.get('/getAllStudents')

def getlist(course:str,age:int):

    courses=[]

    for i in students:
        if i.get('course').casefold() == course.casefold() and i.get('age') == age:
            courses.append(i)
         
    # return courses

# *****************************************************************************************************

# post method -> create

@app.post('/create_student_list')
def create_student_list(details=Body()):
    students.append(details)

# *********************************************************************************************************
# put method --> update    

@app.put('/update_student/list')

def update_list(update=Body()):

    for i in range(len(students)):
        print(i)
        if students[i].get('name').casefold() == update.get('name').casefold():
            students[i]=update


#**********************************************


@app.delete("/delete/list/{param}")
def delete(param :str):
    for i in range(len(students)):
        if students[i].get('name').casefold() == param.casefold():
            students.pop(i)

@app.get("/get_course/")
def getcourselist(course):
    a=[]

    for i in students:
        if i.get('course').casefold() == course.casefold():
            a.append(i)
    return a

@app.get("/get_course/{filter}")
def raj(filter:str):
    a=[]

    for i in students:
        if i.get('course').casefold() == filter.casefold():
            a.append(i)
    return a
