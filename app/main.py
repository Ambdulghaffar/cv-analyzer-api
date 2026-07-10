from fastapi import FastAPI

app = FastAPI(title="CV Analyzer API")

@app.get("/health")
async def health():
    return {"status": "ok"}