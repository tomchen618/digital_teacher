from datetime import datetime

from fastapi import FastAPI, HTTPException

import globle
from globle import app
from model.table_id import Table_Id
import clickhouse_orm as orm


@app.get("/table/{table_name}")
async def get_table_id(table_name: str):
    query_set = Table_Id.objects_in(globle.db).filter(Table_Id.Table == table_name).only("TableId")
    current_id = 0
    if query_set.count() < 1:
        ids = Table_Id.objects_in(globle.db).order_by("-Id").only("Id")
        if ids.count() > 0:
            current_id = ids[0].Id + 1
        else:
            current_id += 1
        table_id = Table_Id(Id=current_id, Table=table_name, TableId=0, Updated=datetime.now())
        globle.db.insert([table_id], batch_size=1)
    else:
        current_id = query_set[0].TableId
    return current_id + 1


@app.post("/table/{table_name}")
async def update_table_id(table_name: str):
    table_id = Table_Id()
    table_id.Table = table_name
    table_id.update_table_id(table_name)


@app.delete("/table/{table_name}")
async def delete_table_id(table_name: str):
    table_id = Table_Id()
    table_id.delete(table_name)
