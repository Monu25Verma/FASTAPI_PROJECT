from  fastapi import FastAPI , Depends, HTTPException, status
from pydantic import BaseModel, Field
import logging
from uuid import UUID   #universal unique id of 128 bit char
import models       #create database table 
from database import engine, SessionLocal #engine-> to start
from sqlalchemy.orm import Session

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)   #disable the loggers that are present when the function is called

log = logging.getLogger(__name__)   # assign loggers with name

#create ne app
app = FastAPI()

#create models in database
models.Base.metadata.create_all(bind=engine)  

#if table not exists create it
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#deserializer/serlializer model
#(database to python in SQL format so to undestand to computer it uses deserialization)
class Book(BaseModel):
    Title : str = Field(min_length=1)
    description : str = Field(min_length=1, max_length=100)
    Author: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)


BOOKS = []

#created url for the book
@app.get("/healthCheck")
def health_check():
    return {"message":"Website Working Succesfully"}


#created url for the book
@app.get("/getBook")
def read_book(db: Session = Depends(get_db)):
    log.info("retrieved data")
    return db.query(models.BookDetails).all()


@app.get("/getBook/{book_id}")
def get_book_id(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(models.BookDetails).filter(models.BookDetails.id == book_id).first()

    if book_model is None :
        log.warn("No data found")
        raise HTTPException(
            status_code = 400, 
            detail= f"ID {book_id} : Does not exist"
        )
    log.info("retrieved data")
    return book_model

    
@app.post("/createBook")
def create_book(book : Book, db: Session = Depends(get_db)):
    book_model = models.BookDetails()
    book_model.Title = book.Title
    book_model.description = book.description
    book_model.Author = book.Author
    book_model.rating = book.rating
    db.add(book_model)
    log.info("Saved data")
    db.commit()
    
    return book


@app.put("/updateBook/{book_id}")
def update_book(book_id: int, book:Book, db: Session = Depends(get_db)):
    book_model = db.query(models.BookDetails).filter(models.BookDetails.id == book_id).first()

    #if none is present in book
    if book_model is None:
        log.warn("No data present")
        raise HTTPException(
            status_code = 404,
            detail= f"ID {book_id} : Does not exist"
        )
    book_model.Title = book.Title
    book_model.description = book.description
    book_model.Author = book.Author
    book_model.rating = book.rating
        
    db.add(book_model)
    log.info("data added")

    db.commit()
    log.info("data saved successfully")
    return book
    

@app.delete("/deleteBook/{book_id}")
def delete_book(book_id: int,  db: Session = Depends(get_db)):
    
    book_model = db.query(models.BookDetails).filter(models.BookDetails.id == book_id)

    if book_model is None:
        log.warn("No data present")
        raise HTTPException(
            status_code= 404,
            detail= f"ID {book_id} : Does not exist"
        )
    
    db.query(models.BookDetails).filter(models.BookDetails.id == book_id).delete()
    db.commit()
    log.info("data save successfully")

    return book_model,status.HTTP_202_ACCEPTED


@app.get("/")
def hello_world():
    log.warn("I got to this point")
    return {"message": "Hello World"}



@app.get("/logdemo")
def sum_num():
    a=4
    b =2
    c = a + b
    log.debug("ouptut after is %d",c)
    d = a - b
    log.info("ouptut after is %d",d)
    e = a / b
    log.warn("ouptut after is %d",e)
    f = a * b
    log.error("ouptut after is %d",f)

    return {"message":"finally Done"} 

