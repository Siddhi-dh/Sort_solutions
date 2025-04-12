from fastapi import FastAPI

# Create a FastAPI application
app = FastAPI()

# Define a simple API endpoint
@app.get("/")
def home():
    return {"message": "API is running!"}
