# models.py


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    descr = Column(String)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    children = relationship("Category", backref="parent", remote_side=[id])
    entries = relationship("Entry", backref="category")

class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    descr = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
