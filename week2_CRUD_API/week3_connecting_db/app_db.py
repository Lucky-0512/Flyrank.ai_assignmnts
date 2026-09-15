from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import pathlib

app = FastAPI()


# Stage 0 — Create your database 

# create a dataabse.
path = pathlib.Path("tasks.db")
if not path.exists():
    with open('tasks.db','a') as f:
        print("created!")
  

# create a sqlite3 cnneciton object.
con = sqlite3.connect('tasks.db',check_same_thread=False)
# lets; create a cursor object to execute SQL queries.
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY,title TEXT NOT NULL,status BOOLEAN DEFAULT FALSE)")

## create three xample tasks is the table is empty.
def create_3(cur):
    read = cur.execute("select * from tasks")
    if read.fetchall() == []:
        cur.execute("INSERT INTO tasks(id,title,status) values(1,'go to running',False),(2,'Wash the car', True),(3,'Write some code', False)")
    else:
        pass


def read_fromdb(cursor):
    d = cursor.execute("SELECT * FROM tasks")
    kk = []
    for k in d.fetchall():
        h = list(k)
        dict_entry = {'id':h[0],'title':h[1],'status':h[2]}
        kk.append(dict_entry)

    return kk   
###########################################################

# let's create a pydantic model, for validating incming equest JSON structre and elemtn datatypes.
class entry(BaseModel):
    id:int
    title:str
    done: bool | None=False

@app.post("/tasks")
def create_task(data:entry):
    task_list = read_fromdb(cur)
    data.id = len(task_list)+1
    data.done = True
    dict_h = {'id':data.id,'title':data.title,"done":data.done}
    if  dict_h=={} or not data.title :
        return {"Bad request" : "task cannot be empty!",
                "status":400}
    cur.execute("INSERT INTO tasks(id,title,status) values(?,?,?)",(dict_h['id'],dict_h['title'],dict_h['done']))
    con.commit()
    return {"Created" : "task created successfully! ",'status':201} 



#############################################################################################33333
# Stage 1: database read endpoints 

@app.get("/tasks")
def get_tasks():
    create_3(cur)
    task_list = read_fromdb(cur)
    return task_list

@app.get("/tasks/{id}")
def get_one(id:int):
    task_list = read_fromdb(cur)

    if id > len(task_list):
        return { "error": "Task 99 not found", 'status':404 }
    return {"data":task_list[id-1],'status':200}
