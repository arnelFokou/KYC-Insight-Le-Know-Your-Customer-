from fastapi import FastAPI, HTTPException

app=FastAPI()

@app.get("/siret/{siret}")
def get_siret(siret):
    pass