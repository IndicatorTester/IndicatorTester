# To set the project directory
import os
import sys
import uvicorn
from fastapi import FastAPI

current_script_path = os.path.abspath(__file__)
project_directory = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_directory)

from activities.CalculateActivity import *

# Define the needed objects
app = FastAPI()
calculateActivity = CalculateActivity()

@app.post('/calculate')
async def calculate(request: CalculateRequest):
    return calculateActivity.act(request)

# Run FastApi server when executing this file
if __name__ == "__main__":
    uvicorn.run("main:app", port=3010, reload=True)