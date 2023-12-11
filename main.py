import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

current_script_path = os.path.abspath(__file__)
project_directory = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_directory)

import activities
import models
import tools

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

@app.post('/calculate')
async def calculate(request: models.CalculateRequest):
    return activities.CalculateActivity.instance().act(request)

@app.post('/calculateExchange')
async def calculate(request: models.CalculateExchangeRequest):
    return activities.CalculateExchangeActivity.instance().act(request)

@app.get('/symbols')
async def getSymbols():
    return activities.GetSymbolsActivity.instance().act()

TOOLS_ACCESS_KEY = '5d0f733d-7fc4-4d3a-bb7d-516c8709f9b5'

@app.get('/ultimateCalculator')
async def runUltimateCalculator(key: str = None):
    if key != TOOLS_ACCESS_KEY:
        raise HTTPException(status_code=403, detail='Access Denied')
    return tools.UltimateCalculator.instance().run()

if __name__ == "__main__":
    uvicorn.run("main:app", port=3010, reload=True)