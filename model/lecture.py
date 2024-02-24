from datetime import datetime

from clickhouse_orm import Model, StringField, Int32Field, DateTimeField, F, MergeTree
from pydantic import BaseModel


class Lecture(Model):
    """
    Lecture Id
    """
    id = Int32Field(default=0)
    """
    Lecture Name
    """
    name = StringField(default="")
    """
    Lecture Title
    """
    title = StringField(default="")
    """
    Lecture Total Pages
    """
    pages = Int32Field(default=0)
    """
    File Lecture Created from 
    """
    created_from_file = StringField(default="")
    """
    Author
    """
    author = StringField(default="")
    """
    Original Lang 
    """
    origin_lang = StringField(default="ZH")
    """
    Lecture Lang
    """
    default_lang = StringField(default="EN")
    """
    Lecture Creator
    """
    created_by = StringField(default="")
    """
    Lecture Modifier
    """
    updated_by = StringField(default="")
    """
    Created Datetime
    """
    created = DateTimeField(default=F.now())
    """
    Update Datetime
    """
    updated = DateTimeField(default=F.now())
    """
    Description
    """
    description = StringField(default="")

    engine = MergeTree('created', ('id', 'name', 'created_by'))


class Lecture_View(Model):
    """
    Lecture Id
    """
    id: str
    """
    Lecture Name
    """
    name: str
    """
    Lecture Title
    """
    title: str
    """
    Lecture Total Pages
    """
    pages: int
    """
    File Lecture Created from 
    """
    created_from_file: str
    """
    Author
    """
    author: str
    """
    Original Lang 
    """
    origin_lang: str = "ZH"
    """
    Lecture Lang
    """
    default_lang: str = "EN"
    """
    Lecture Creator
    """
    created_by: str
    """
    Lecture Modifier
    """
    updated_by: str
    """
    Created Datetime
    """
    created: datetime
    """
    Update Datetime
    """
    updated: datetime
    """
    Description
    """
    description: str
