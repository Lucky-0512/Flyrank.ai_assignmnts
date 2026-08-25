from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

'''@app.get("/")
def greet():
    return {'msg':"Hello Server!!" ,'status': 200}'''

@app.get("/")
def itemslo():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }    

class entry(BaseModel):
    id:int
    title:str
    done: bool


@app.get("/health")
def health():
    return {'status':'OK'}

## stage 2
memory:list[dict] = [
    {'id':1,'title':"finish my assigemtn , i wanna fly to bosnia ;).","done":False},
    {'id':2,'title':"do chores .","done":False},
    {'id':3,'title':"walk out to the park","done":True}
]

@app.get("/tasks")
def get_tasks():
    return memory

@app.get("/tasks/{id}")
def get_one(id:int):
    if id > len(memory):
        return { "error": "Task 99 not found", 'status':404 }
    return {"data":memory[id-1],'status':200}


