import os
import sys
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

current_script_path = os.path.abspath(__file__)
project_directory = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_directory)

from utils.AuthUtils import AuthUtils
import activities
import models
import tools

app = FastAPI()
authUtils = AuthUtils.instance()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def health():
    return {'message': 'healthy'}

async def validateAccess(Auth: str = Header(None, convert_underscores=False)):
    if not (await authUtils.isUserLoggedIn(Auth)):
        raise HTTPException(status_code=403, detail='Access Denied')

@app.post('/calculate')
async def calculate(request: models.CalculateRequest, Auth: str = Depends(validateAccess)):
    return activities.CalculateActivity.instance().act(request)

TOOLS_ACCESS_KEY = '5d0f733d-7fc4-4d3a-bb7d-516c8709f9b5'

@app.get('/ultimateCalculator')
async def runUltimateCalculator(key: str = None):
    if key != TOOLS_ACCESS_KEY:
        raise HTTPException(status_code=403, detail='Access Denied')
    return tools.UltimateCalculator.instance().run()

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("main:app", host='0.0.0.0', port=3010, reload=os.getenv("DEBUG", False))