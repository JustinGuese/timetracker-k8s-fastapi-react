from typing import List

from db import TimeEntryDB, TimeEntryInfo, TimerEnd, TimerStart, get_db
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()

TIMER_MEMORY = {
    "hpe" : {
        "running" : False,
        "start_time" : None,
    },
    "bw" : {
        "running" : False,
        "start_time" : None,
    }
}

@app.get("/timer/clients", response_model=List[str])
async def get_clients():
    clients = [str(client) for client in TIMER_MEMORY.keys()]
    return clients

@app.get("/timer/info", response_model=List[TimeEntryInfo])
async def timer_info():
    response = []
    for key in TIMER_MEMORY.keys():
        entry = TimeEntryInfo(
            customer = key,
            running = TIMER_MEMORY[key]["running"],
            start_time = TIMER_MEMORY[key]["start_time"]
        )
        response.append(entry)
    return response

@app.put("/timer/start/")
async def start_timer(timerstart: TimerStart):
    if timerstart.customer not in TIMER_MEMORY:
        raise HTTPException(status_code=404, detail="customer not found. valid options are: " + ", ".join(TIMER_MEMORY.keys()))
    # check if timer is already running, deny if so
    if TIMER_MEMORY[timerstart.customer]["running"]:
        raise HTTPException(status_code=400, detail="timer already running. you can't overwrite it")
    TIMER_MEMORY[timerstart.customer]["running"] = True
    TIMER_MEMORY[timerstart.customer]["start_time"] = timerstart.start_time
    
@app.put("/timer/stop/")
async def start_timer(timerstart: TimerEnd, db: Session = Depends(get_db)):
    if timerstart.customer not in TIMER_MEMORY:
        raise HTTPException(status_code=404, detail="customer not found. valid options are: " + ", ".join(TIMER_MEMORY.keys()))
    # check if timer is already running, deny if so
    if not TIMER_MEMORY[timerstart.customer]["running"]:
        raise HTTPException(status_code=400, detail="timer not running. you can't end it before it started")
    # else construct db object
    timeDbObj = TimeEntryDB(
        customer = timerstart.customer,
        start_time = TIMER_MEMORY[timerstart.customer]["start_time"],
        end_time = TIMER_MEMORY[timerstart.customer]["end_time"],
        duration_hours = (TIMER_MEMORY[timerstart.customer]["end_time"] - TIMER_MEMORY[timerstart.customer]["start_time"]).total_seconds() / 3600
    )
    try:
        db.add(timeDbObj)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="could not save to database: " + str(e))