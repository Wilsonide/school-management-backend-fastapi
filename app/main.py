from app.api.v1.router import api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="LERNA API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "LERNA backend running 🚀"}
