from clickhouse_orm import *
from pydantic import BaseModel

import globle


class Table_Id(Model):
    """
    Id table key
    """
    Id = Int32Field(default=0)
    """
    Table Name
    """
    Table = StringField(default="table_id")
    """
    Current Table Id
    """
    TableId = UInt32Field(default=1)
    """
    Updated Time
    """
    Updated = DateTimeField(default=F.now())

    engine = MergeTree('Updated', ('Id', 'Table', 'TableId'))

    @classmethod
    def insert_table(cls, table):
        sel = cls.objects_in(globle.db).filter(Id=0)
        if sel.count() > 0:
            id = sel[0].TableId + 1
            sel.update(TableId=id)
            new_table = cls(Id=id, Table=table, TableId=1)
            globle.db.insert([new_table, ])

    @classmethod
    def update_table_id(cls, table: str):
        sel = cls.objects_in(globle.db).filter(Table=table)
        if sel.count() < 1:
            cls.insert_table(table)
            return 1
        else:
            id = sel[0].TableId + 1
            sel.update(TableId=id)
            return id

    @classmethod
    def table_name(cls):
        return 'table_id'

    @classmethod
    def insert(cls, id: int):
        cls.Id = id
        globle.db.insert([cls, ])

    @classmethod
    def update(cls):
        sel = cls.objects_in(globle.db).filter(id=cls.Id)
        if sel.count() == 1:
            sel.update(TableId=sel[0].TableId)

    @classmethod
    def delete(cls, table_name: str):
        sel = cls.objects_in(globle.db).filter(Table=table_name)
        sel.delete()


class Table_Id_View(BaseModel):
    """
    Id table key
    """
    id: int
    """
    Table Name
    """
    table: str
    """
    Current Table Id
    """
    table_id: int
    # """
    # Updated
    # """
    # updated: DateTimeField
