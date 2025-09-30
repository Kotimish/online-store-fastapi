import uvicorn
from fastapi import FastAPI
from routers.main_router import router as main_router

app = FastAPI()
app.include_router(main_router)

if __name__=="__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
