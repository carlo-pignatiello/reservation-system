from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes import order_router
from app.exceptions import CustomException
import uvicorn

app = FastAPI()

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"error_code": exc.error_code, "message": exc.message},
    )

app.include_router(order_router)

if __name__ == "__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=4557, reload=True)