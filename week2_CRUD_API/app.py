from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def greet():
    return {'msg':"Hello Server!!" ,'status': 200}