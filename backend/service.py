from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def health():
    return {"message": "pong"}
