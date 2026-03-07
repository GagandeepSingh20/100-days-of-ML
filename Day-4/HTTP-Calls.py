from fastapi import FastAPI
import json

app=FastAPI()

def load_data():
    with open('patient_dataset.json','r') as f:
        data=json.load(f)

    return data

@app.get("/")
def hello():
    return{'message': 'API of Patients'}

@app.get("/about")
def about():
    return {'message':'A fully functional API to manage your patient history'}

@app.get("/view")
def view():
    data=load_data()
    return data
