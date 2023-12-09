import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

current_script_path = os.path.abspath(__file__)
project_directory = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_directory)

import activities
import models

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

calculateActivity = activities.CalculateActivity.instance()
calculateExchangeActivity = activities.CalculateExchangeActivity.instance()

getSymbolsActivity = activities.GetSymbolsActivity.instance()

@app.post('/calculate')
async def calculate(request: models.CalculateRequest):
    return calculateActivity.act(request)

@app.post('/calculateExchange')
async def calculate(request: models.CalculateExchangeRequest):
    return calculateExchangeActivity.act(request)

@app.get('/symbols')
async def getSymbols():
    return getSymbolsActivity.act()

if __name__ == "__main__":
    uvicorn.run("main:app", port=3010, reload=True)