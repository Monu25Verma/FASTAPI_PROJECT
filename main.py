from  fastapi import FastAPI
import logging

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

log = logging.getLogger(__name__)
app = FastAPI()

@app.get("/")
def hello_world():
    log.warn("I got to this point")
    return {"message": "Hello World"}

@app.get("/logdemo")
def sum_num():
    a=4
    b =2
    c = a + b
    d = a - b
    e = a / b
    f = a * b
    log.debug("ouptut after is %f",c)
    log.info("ouptut after is %f",d)
    log.warn("ouptut after is %f",e)
    log.error("ouptut after is %f",f)
    return {"message":"finally Done"}

