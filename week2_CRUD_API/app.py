from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

'''@app.get("/")
def greet():
    return {'msg':"Hello Server!!" ,'status': 200}'''

@app.get("/")
def itemslo():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }    

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


## stage 3

# let's create a pydantic model, for validating incming equest JSON structre and elemtn datatypes.
class entry(BaseModel):
    id:int | None=None
    title:str
    done: bool | None=None

@app.post("/tasks")
def create_task(data:entry):
    data.id = len(memory)+1
    data.done = True
    dict_h = {'id':data.id,'title':data.title,"done":data.done}
    if  dict_h=={} or not data.title :
        return {"Bad request" : "task cannot be empty!",
                "status":400}
    memory.append(dict_h)
    return {"Created" : "task created successfully! ",'status':201} 

## stage 4

@app.put("/tasks/{id}")
def update(data:entry,id:int):

    if id > len(memory) or id not in memory[id-1].values():
        return {"Unknown ID":404}

    else:
        if data.title:
            ##now update the title.
            memory[id-1]["title"] = data.title

        elif data.done:
            ## pdate the task status.
            memory[id-1]["done"] = data.done      

    return memory[id-1]        


@app.delete("/tasks/{id}")
def del_task(id:int):
    if id > len(memory) or id not in memory[id-1].values():
        return {"Unknown ID, cant delete":404}

    memory.remove(memory[id-1])
    return {f"task {id} Deleted Successfully!":200}
    
### FULL CRUD COMPLETE!
         
    
    

