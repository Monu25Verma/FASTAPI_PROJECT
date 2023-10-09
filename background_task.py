from  fastapi import FastAPI , Depends, HTTPException, status, BackgroundTasks
app = FastAPI()
def notification_email(email: str, message = ""):
    #in python format way to write python write function
    with open("log.txt", mode= 'w') as email_file:   #to save in file made by them so we have to give name
        content = f"notification_email for {email}:{message}"
        email_file.write(content)
    with open("log.txt", mode= 'r') as email_file:
        print(email_file.read())


@app.post("/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(notification_email, email, message="some notification")
    return {"message": "Notification sent in the background"}


