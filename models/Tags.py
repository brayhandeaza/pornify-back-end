from sqlmodel import SQLModel, Field
from datetime import datetime


class Tags(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        super().save(*args, **kwargs)