from fastapi import FastAPI, Header, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from orjson import loads, dumps

from typing import Annotated
from os.path import isfile
from pathlib import Path
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

if not isfile("data.json"):
    p = Path("data.json")
    p.touch()
    p.write_text("[[],[],[],[],[],[],[],[],[],[],[],[],[]]")

with open('data.json', 'rb') as f:
    data_cont: list[dict] = loads(f.read())

@app.post("/data/{month}/{typeofcof}")
def post_data(
    typeofcof: str,
    month: int,
    data: Annotated[int | None, Header()] = None
):
    if data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    data_cont[month-1].append({"type": typeofcof, "data": data})
    with open('data.json', 'wb') as f:
        f.write(dumps(data_cont))

@app.get("/data/{month}")
def get_data(month: int):
    return JSONResponse(sum(item["data"] for item in data_cont[month-1]), headers={"Access-Control-Allow-Origin": "*"})

@app.get("/data/{month}/{typeofcof}")
def get_data_by_type(month: int, typeofcof: str):
    return JSONResponse(sum(item["data"] for item in data_cont[month-1] if item["type"] == typeofcof), headers={"Access-Control-Allow-Origin": "*"})
