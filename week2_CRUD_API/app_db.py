from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

from pathlib import Path

file_db = Path("tasks.db")
if not file_db.exists():
    # crate the file.
    f1 = open('tasks.db','a')
    
## let's cteate a db connection object.
conn= sqlite3.connect("tasks.db")
cur = conn.cursor() # it is sing this object we prfomr the SQLITE3 commnds.

# let's create a table.
cur.execute(' CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,done INTEGER DEFAULT 0)')
conn.commit() # apply changes.
conn.close()

app = FastAPI()  # create the fastapi instance.


# now let' insert the  3 values.
entries = [{'title':'do the utensils'},
            {'title':'do the cooking','done':True},
            {'title':'take the dog out for a walk','done':True}]


def insert_tasks(entries:list[dict]):
    conn= sqlite3.connect("tasks.db")
    cur = conn.cursor() # it is sing this object we prfomr the SQLITE3 commnds.

    count = cur.execute("SELECT count(*) from tasks").fetchone()[0]
    if count != 0:
        # flush all rows.
        cur.execute("DELETE from tasks")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='tasks'") ## flush all autovalues
        conn.commit() ## apply changes

    for j in entries:
        if 'done' not in j.keys() or j['done'] == False:
            j['done'] = 0
            cur.execute(f'INSERT into tasks("title","done") values(?,?)',(j['title'],j['done']))

        else:
            j['done'] = 1
            cur.execute(f'INSERT into tasks("title","done") values(?,?)',(j['title'],j['done']))
                   
    
        conn.commit()
    conn.close()


## first we ru this command to insert the 3 tasks by default.
insert_tasks(entries)


@app.get("/tasks")
def get_tasks():
    conn= sqlite3.connect("tasks.db")
    cur = conn.cursor() # it is sing this object we prfomr the SQLITE3 commnds.

    
    ## just fetch th tasks.
    get_data = cur.execute("SELECT * from tasks")
    dee = []
    for k in get_data:
        dee.append(k)

    conn.close()    

    return dee    

 




    
    

