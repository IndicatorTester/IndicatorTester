import os
import sys
import uvicorn
from fastapi import FastAPI

current_script_path = os.path.abspath(__file__)
project_directory = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_directory)

import activities
import models

app = FastAPI()
calculateActivity = activities.CalculateActivity.instance()

@app.post('/calculate')
async def calculate(request: models.CalculateRequest):
    return calculateActivity.act(request)

if __name__ == "__main__":
    uvicorn.run("main:app", port=3010, reload=True)