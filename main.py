import os
import sys
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging

current_script_path = os.path.abspath(__file__)
project_directory = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_directory)
logging.basicConfig(level=logging.INFO)

from utils import AuthUtils
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

def validateAccess(request: Request):
    if not authUtils.hasAccess(dict(request.headers)):
        logging.warn(f"Invalid auth header: [{dict(request.headers)['auth']}]")
        raise HTTPException(status_code=403, detail='Access Denied')

@app.post('/calculate')
async def calculate(request: models.CalculateRequest, Auth: str = Depends(validateAccess)):
    return activities.CalculateActivity.instance().act(request)

@app.get('/user')
async def user(userId: str, Auth: str = Depends(validateAccess)):
    return activities.GetUserActivity.instance().act(userId)

@app.put('/user')
async def user(request: models.UpdateUserRequest, Auth: str = Depends(validateAccess)):
    return activities.UpdateUserActivity.instance().act(request)

@app.get('/testArchive')
async def testArchive(userId: str, timestamp: str, pageNumber: int, Auth: str = Depends(validateAccess)):
    return activities.GetTestArchiveActivity.instance().act(
        userId=userId,
        timestamp=timestamp,
        pageNumber=pageNumber
    )

@app.get('/testActions')
async def testActions(userId: str, timestamp: str, Auth: str = Depends(validateAccess)):
    return activities.GetTestActionsActivity.instance().act(
        userId=userId,
        timestamp=timestamp
    )

@app.post('/sendFeedback')
async def sendFeedback(request: models.SendFeedbackRequest, Auth: str = Depends(validateAccess)):
    return activities.SendFeedbackActivity.instance().act(request)

@app.get('/payment')
async def payment(userId: str, priceId: str, Auth: str = Depends(validateAccess)):
    return activities.UserPaymentActivity.instance().act(
        userId=userId,
        priceId=priceId
    )

TOOLS_ACCESS_KEY = '7654a285-b65e-4577-aeac-cc720a30ca37'

@app.get('/ultimateCalculator')
async def runUltimateCalculator(key: str = None):
    if key != TOOLS_ACCESS_KEY:
        raise HTTPException(status_code=403, detail='Access Denied')
    return tools.UltimateCalculator.instance().run()

@app.get('/autoTrader')
async def runAutoTrader(key: str = None):
    if key != TOOLS_ACCESS_KEY:
        raise HTTPException(status_code=403, detail='Access Denied')
    return tools.AutoTrader.instance().trade()

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("main:app", host='0.0.0.0', port=3010, reload=os.getenv("DEBUG", False))