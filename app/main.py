from fastapi import FastAPI

app = FastAPI(
    title="EasyAttend API",
    description="Local-first attendance companion",
    version="0.1.0"
)

@app.get("/health")
def check_health():
    return {"status": "healthy", "app": "EasyAttend", "version": "0.1.0"}

@app.get("/")
def greet():
    return {"message" : "Welcome to the BuggyAssist"}