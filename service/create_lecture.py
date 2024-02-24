from fastapi import FastAPI, HTTPException

from globle import app
from model.lecture import Lecture


@app.post("/lecture/")
async def create_lecture(lecture: str):
    item_dict = Lecture.dict()

    # Assign a unique ID to the item (for demonstration purposes)
    item_dict['id'] = len(db) + 1

    # Store the item in the "database"
    db.append(item_dict)

    # Return the created item
    return item_dict
    
    return {"Hello": "World"}
