from sqlalchemy import Integer, String, Column
from database import Base


class BookDetails(Base):

    __tablename__ = 'books'
    id = Column(Integer, primary_key = True, index = True)
    Title = Column(String)
    description = Column(String)
    Author = Column(String)
    rating = Column(Integer)
