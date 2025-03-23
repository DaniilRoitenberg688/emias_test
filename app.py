from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from routes.user import router as users_router
from routes.p_doc import router as p_docs_router
from routes.i_doc import router as i_doc_router
from routes.patient import router as patient_router
from fastapi.exceptions import RequestValidationError

app = FastAPI()


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#    print(exc)
#    raise HTTPException(status_code=400, detail="wrong data")

@app.get("/ping")
async def ping():
    return {"message": "pong"}


app.include_router(users_router)
app.include_router(p_docs_router)
app.include_router(i_doc_router)
app.include_router(patient_router)
